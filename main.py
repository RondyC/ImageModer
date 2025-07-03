from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DEEP_AI_API_KEY = os.getenv("DEEP_AI_API_KEY")
if not DEEP_AI_API_KEY:
    raise RuntimeError("Переменная окружения DEEP_AI_API_KEY не найдена")

NSFW_THRESHOLD = 0.7


@app.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Формат файла не поддерживается. Загрузите JPEG или PNG.")

    try:
        image_data = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Не удалось прочитать файл")

    try:
        response = requests.post(
            "https://api.deepai.org/api/nsfw-detector",
            files={"image": (file.filename, image_data)},
            headers={"api-key": DEEP_AI_API_KEY},
            timeout=15
        )
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ошибка при обращении к DeepAI: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="DeepAI вернул ошибку")

    try:
        result = response.json()
        nsfw_score = result.get("output", {}).get("nsfw_score")
        if nsfw_score is None:
            raise ValueError("Отсутствует nsfw_score")
    except Exception:
        raise HTTPException(status_code=500, detail="Некорректный ответ от DeepAI")

    if nsfw_score > NSFW_THRESHOLD:
        return {"status": "REJECTED", "reason": "NSFW content"}

    return {"status": "OK"}