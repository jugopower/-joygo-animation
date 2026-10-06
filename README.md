# Joy Go Animation Beta 0.3

完全免費的獨立 MP4 測試版，不連接 Joy Go Platform，也不使用 Replicate/API Token。

## 功能
- 上傳人物照片
- 慢慢推近、左右移動、柔和推近
- 5 秒或 10 秒 MP4
- 直接在網頁預覽

## Render
Build Command: `pip install -r requirements.txt`

Start Command: `gunicorn app:app`

不需要 Environment Variable。原本的 `REPLICATE_API_TOKEN` 可以刪除。

> Beta 0.3 是照片鏡頭動畫，不是生成式 AI 人物動畫，因此人物不會真正眨眼、說話或揮手。
