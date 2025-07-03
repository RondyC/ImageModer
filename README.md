# FastAPI Image Moderation via DeepAI

## Эндпоинт
`POST /moderate`  
Загружается изображение `.jpg`, `.png`  
Модерация выполняется через DeepAI NSFW Detector API

### Ответ:
- `{"status": "OK"}` — безопасно
- `{"status": "REJECTED", "reason": "NSFW content"}` — неприемлемый контент

# Проверка

## Установка
pip install -r requirements.txt

## Запуск 
uvicorn main:app --reload

## Интерфейс
http://localhost:8000/docs