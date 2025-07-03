# FastAPI Image Moderation by DeepAI

## Эндпоинт
`POST /moderate`  
Загружается изображение `.jpg`, `.png`  
Модерация выполняется через DeepAI NSFW Detector API

### Ответ:
- `{"status": "OK"}` — безопасно
- `{"status": "REJECTED", "reason": "NSFW content"}` — неприемлемый контент

# Подготовка
Перед использованием вписать ключ!

## Установка
pip install -r requirements.txt

## Запуск 
uvicorn main:app --reload

## Интерфейс
http://localhost:8000/docs

# Примеры запросов

## Curl
curl -X POST http://127.0.0.1:8000/moderate \
  -H "accept: application/json" \
  -F "file=@test_image.jpg" # При условии, если файл находится рядом с проектом

## Postman

### Настройка запроса:
Method: POST
URL: http://127.0.0.1:8000/moderate

### Вкладка Body:
Выберите тип: form-data
Добавьте поле:
Key: file
Type: File
Value: выберите изображение .jpg или .png на диске

### Вкладка Headers:
Проверить, что автоматически добавлено:
Content-Type: multipart/form-data

### Примеры ответов:
1. Положительный результат
{
  "status": "OK"
}

2. Неприемлемый контент
{
  "status": "REJECTED",
  "reason": "NSFW content"
}
