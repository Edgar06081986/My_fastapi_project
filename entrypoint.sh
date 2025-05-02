#!/bin/bash

echo "⏳ Ожидание PostgreSQL на postgainer:5432..."
while ! nc -z postgainer 5432; do
  sleep 1
done
echo "✅ PostgreSQL доступен!"
echo "⏳ Запуск миграций Alembic..."
alembic upgrade head || { echo "❌ Миграции не применены"; exit 1; }

echo "✅ Миграции применены. Запуск FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
