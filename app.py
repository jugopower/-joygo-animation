import os, tempfile
from flask import Flask, request, jsonify, send_from_directory
import replicate

app = Flask(__name__, static_folder=".", static_url_path="")

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/generate")
def generate():
    if not os.getenv("REPLICATE_API_TOKEN"):
        return jsonify(error="伺服器尚未設定 REPLICATE_API_TOKEN。"), 500
    photo=request.files.get("photo")
    if not photo:
        return jsonify(error="沒有收到人物照片。"),400
    prompt=request.form.get("prompt","人物坐在圍棋盤前自然微笑")
    duration=int(request.form.get("duration","5"))
    suffix=os.path.splitext(photo.filename or ".jpg")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as f:
        photo.save(f.name); path=f.name
    try:
        with open(path,"rb") as image:
            output=replicate.run("wan-video/wan-2.6-i2v", input={
                "image": image,
                "prompt": prompt,
                "duration": duration
            })
        url=output.url() if hasattr(output,"url") else str(output)
        return jsonify(video_url=url)
    except Exception as e:
        return jsonify(error=f"影片生成失敗：{e}"),500
    finally:
        try: os.remove(path)
        except: pass

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","10000")))
