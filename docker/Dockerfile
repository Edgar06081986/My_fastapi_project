FROM python:3.12-slim

# Установка системных зависимостей для сборки Python-пакетов
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка утилиты uv (пакетный менеджер)
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Установка зависимостей
COPY pyproject.toml uv.lock ./
ENV UV_SYSTEM_PYTHON=1
RUN uv pip install --system --no-cache -r pyproject.toml

# Удаление ненужных теперь компиляторов и заголовков (опционально)
RUN apt-get purge -y --auto-remove gcc python3-dev build-essential

# Копируем весь проект
COPY . /app
WORKDIR /app

# Чтобы модуль src правильно импортировался
ENV PYTHONPATH=/app

# Установка netcat (если нужно)
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Запуск FastAPI через uvicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
