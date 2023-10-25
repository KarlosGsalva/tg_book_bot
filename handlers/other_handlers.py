from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

router = Router()


@router.message(F.text == 'Создай кнопку start')
async def to_create_start_button(message: Message):
    if message.from_user.id == '1074713049':
        kb = [[KeyboardButton(text='/start')]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Кнопка создана', reply_markup=keyboard)
    else:
        await message.answer(text='Это команда доступная только администраторам')


@router.message(F.text == 'Удали клавиатуру')
async def to_delete_keyboard(message: Message):
    if message.from_user.id == '1074713049':
        await message.reply(text='Клавиатура удалена', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text='Это команда доступная только администраторам')


@router.message()
async def send_echo(message: Message):
    await message.answer(f"Извините, мне не знакома эта команда '{message.text}',"
                         f"используйте /help для получения списка команд")
