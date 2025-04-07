# Используем официальный образ Python
FROM python:3.9-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости и исходный код
COPY requirements.txt .
COPY ./app /app/app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]