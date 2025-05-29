import logging
import os

# Убедись, что папка logs существует
os.makedirs("logs", exist_ok=True)

# Настройка логирования
logging.basicConfig(
    filename="logs/app.log",  # путь относительно корня проекта
    filemode="a",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
