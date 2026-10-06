import os, tempfile, subprocess, uuid
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image, ImageOps
import imageio_ffmpeg

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'generated')
os.makedirs(OUT, exist_ok=True)
app = Flask(__name__, static_folder=BASE, static_url_path='')

@app.get('/')
def home():
    return send_from_directory(BASE, 'index.html')

@app.get('/generated/<path:name>')
def generated(name):
    return send_from_directory(OUT, name, mimetype='video/mp4')

@app.post('/api/generate')
def generate():
    photo = request.files.get('photo')
    if not photo:
        return jsonify(error='請先選擇人物照片。'), 400
    try:
        duration = max(3, min(10, int(request.form.get('duration', '5'))))
    except ValueError:
        duration = 5
    effect = request.form.get('effect', 'zoom')
    work = tempfile.mkdtemp(prefix='joygo_')
    src = os.path.join(work, 'source.jpg')
    out_name = f'joygo-{uuid.uuid4().hex[:10]}.mp4'
    out_path = os.path.join(OUT, out_name)
    try:
        img = Image.open(photo.stream).convert('RGB')
        img = ImageOps.exif_transpose(img)
        # 16:9 HD frame, crop from center so phone photos also work.
        img = ImageOps.fit(img, (1280, 720), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        img.save(src, 'JPEG', quality=94)
        fps = 30
        frames = duration * fps
        if effect == 'pan':
            vf = f"zoompan=z='1.08':x='(iw-iw/zoom)*on/{frames}':y='(ih-ih/zoom)/2':d={frames}:s=1280x720:fps={fps},fade=t=in:st=0:d=.5,fade=t=out:st={max(0,duration-.6)}:d=.6,format=yuv420p"
        elif effect == 'gentle':
            vf = f"zoompan=z='1.03+0.00018*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s=1280x720:fps={fps},fade=t=in:st=0:d=.5,fade=t=out:st={max(0,duration-.6)}:d=.6,format=yuv420p"
        else:
            vf = f"zoompan=z='min(zoom+0.00045,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps={fps},fade=t=in:st=0:d=.5,fade=t=out:st={max(0,duration-.6)}:d=.6,format=yuv420p"
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg, '-y', '-loop', '1', '-i', src, '-vf', vf, '-t', str(duration), '-r', str(fps), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-movflags', '+faststart', out_path]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
        if p.returncode != 0:
            return jsonify(error='MP4 製作失敗：' + p.stderr[-800:]), 500
        return jsonify(video_url=f'/generated/{out_name}')
    except Exception as e:
        return jsonify(error=f'MP4 製作失敗：{e}'), 500
    finally:
        try:
            if os.path.exists(src): os.remove(src)
            os.rmdir(work)
        except Exception:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '10000')))
