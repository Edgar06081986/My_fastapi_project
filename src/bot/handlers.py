from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.models import JewelersOrm

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я Мой Ювелир бот.")


@router.message(Command("help"))
async def handle_help(message: types.Message):
    text = "Я Мой Ювелир бот.\nОтправь мне какое нибудь сообщение!"
    await message.answer(text=text)


@router.message(Command("jewelers"))
async def get_jewelers_handler(message: types.Message, session: AsyncSession):
    result = await session.execute(select(JewelersOrm))
    jewelers = result.scalars().all()
    if not jewelers:
        await message.answer("Ювелиры не найдены.")
        return

    text = "\n".join([f"{j.name} — {j.city}" for j in jewelers])
    await message.answer(f"💎 Список ювелиров:\n{text}")
