from aiogram import Bot, Dispatcher
from src.bot.handlers import router
import src.config as config
from src.logger import logger
from src.database import async_session_factory
from src.bot.middlewares.db_session import DBSessionMiddleware


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Подключаем middleware сессии
dp.message.middleware(DBSessionMiddleware(async_session_factory))


async def start_bot():
    logger.info()
    await dp.start_polling(bot)
