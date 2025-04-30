FROM python:3.12-slim

# Установка утилиты uv (пакетный менеджер)
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Установка зависимостей
COPY pyproject.toml uv.lock ./
ENV UV_SYSTEM_PYTHON=1
RUN uv pip install --system --no-cache -r pyproject.toml

# Копируем весь проект
COPY . /app
WORKDIR /app

# Чтобы модуль src правильно импортировался
ENV PYTHONPATH=/app

# Запуск FastAPI через uvicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]


#FROM python:3.12-slim
#
#RUN apt-get update
#
## install uv
#COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/
#
#COPY pyproject.toml uv.lock ./
#
#ENV UV_SYSTEM_PYTHON=1
#
## install deps to global python
#RUN uv pip install --system --no-cache -r pyproject.toml
#
#WORKDIR /api_v1
#
#ENV PYTHONPATH=/app


## Используем официальный образ Python
#FROM python:3.9-slim
#
## Рабочая директория в контейнере
#WORKDIR /app
#
## Копируем зависимости и исходный код
#COPY requirements.txt .
#COPY ./app /app/app
#
## Устанавливаем зависимости
#RUN pip install --no-cache-dir -r requirements.txt
#
## Команда для запуска сервера
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]