from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()
print("KEY:", os.getenv("DEEP_AI_API_KEY"))

app = FastAPI()

DEEP_AI_API_KEY = os.getenv("DEEP_AI_API_KEY")

if not DEEP_AI_API_KEY:
    raise RuntimeError("DEEP_AI_API_KEY is not set in .env")

@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    # Проверка расширения файла
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Only .jpg and .png files are allowed")

    # Чтение изображения
    image_bytes = await file.read()

    # Запрос к DeepAI
    response = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={"image": (file.filename, image_bytes)},
        headers={"api-key": DEEP_AI_API_KEY}
    )

    print("DeepAI status code:", response.status_code)
    print("DeepAI response body:", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to connect to DeepAI API")

    try:
        nsfw_score = response.json()["output"]["nsfw_score"]
    except (KeyError, TypeError):
        raise HTTPException(status_code=500, detail="Invalid response format from DeepAI")

    # Возврат результата
    if nsfw_score > 0.7:
        return {"status": "REJECTED", "reason": "NSFW content"}
    return {"status": "OK"}