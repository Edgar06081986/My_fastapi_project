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

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Запуск FastAPI через uvicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

