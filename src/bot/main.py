from aiogram import Bot, Dispatcher
from src.bot.handlers import router
import src.config as config
from src.logger import logger
from src.models.db_helper import db_helper
from src.bot.middlewares.db_session import DBSessionMiddleware


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Подключаем middleware сессии
dp.message.middleware(DBSessionMiddleware(db_helper.scoped_session_dependency))


async def start_bot():
    logger.info()
    await dp.start_polling(bot)
