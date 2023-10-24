from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, user_db
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData, IsInlinebuttonWithSlash
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()


# хэндлер для обработки команды /start, добавления пользователя в БД
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)


# хэндлер для обработки /help и отправки доступных команд
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# хэндлер команды /beginning и отправки первой страницы книги с пагинацией
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    user_db[message.from_user.id]['page'] = 1
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
         'backward',
         f'{user_db[message.from_user.id]["page"]}/{len(book)}',
         'forward'))


# хэндлер срабатывает на /continue и отправлять пользователю страницу книги
# на которой пользователь остановился
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{user_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'))


# хэндлер команды /bookmarks, отправляет пользователю список сохраненных закладок
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if user_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *user_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# хэндлер для обработки инлайн-кнопки "вперед"
@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(book):
        user_db[callback.from_user.id]['page'] += 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f"{user_db[callback.from_user.id]['page']}/{len(book)}",
                'forward'))
    await callback.answer()


# хэндлер для обработки инлайн-кнопки "назад"
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f"{user_db[callback.from_user.id]['page']}/{len(book)}",
                'forward'))
    await callback.answer()


# хэндлер для обработки инлайн-кнопки с номером текущей страницы и добавления
# ее в закладки
@router.callback_query(IsInlinebuttonWithSlash())
async def process_page_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].add(
        user_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


# хэндлер будет срабатывать на нажатие инлайн-кнопки с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    user_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'))
    await callback.answer()


# хэндлер нажатия инлайн-кнопки "редактировать" под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *user_db[callback.from_user.id]['bookmarks']))
    await callback.answer()


# хэндлер нажатия инлайн-кнопки "отменить" во время работы со списком закладок
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# хэндлер нажатия инлайн-кнопки с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *user_db[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
