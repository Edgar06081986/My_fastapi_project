from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я Мой Ювелир бот.")


@router.message(Command("help"))
async def handle_help(message: types.Message):
    text = "Я Мой Ювелир бот.\nОтправь мне какое нибудь сообщение!"
    await message.answer(text=text)
