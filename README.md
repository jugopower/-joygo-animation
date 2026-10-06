# Joy Go Animation Beta 0.2

獨立 MP4 實測版，不連接 Joy Go Platform。

## 功能
- 上傳朱老師照片
- 輸入人物動作
- 產生 5 或 10 秒測試 MP4
- 使用 Replicate 的 Wan image-to-video 模型
- API Token 只存在伺服器環境變數

## Render 測試設定
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

Environment:
REPLICATE_API_TOKEN = 你的 Replicate API Token

注意：影片 AI 服務可能產生費用，是否有免費額度由服務商帳號狀態決定。
