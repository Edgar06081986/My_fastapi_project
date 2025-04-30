#!/bin/bash
echo "⏳ Запуск миграций Alembic..."
alembic upgrade head

echo "✅ Миграции применены. Запуск FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
