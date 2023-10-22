from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def send_echo(message: Message):
    await message.answer(f"Извините, мне не знакома эта команда '{message.text}',"
                         f"используйте /help для получения списка команд")

