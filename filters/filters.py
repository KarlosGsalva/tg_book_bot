from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()


class IsInlinebuttonWithSlash(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return '/' in callback.data and callback.data.replace('/', '').isdigit()
