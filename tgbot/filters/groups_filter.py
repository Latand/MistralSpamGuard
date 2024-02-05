from aiogram import types
from aiogram.filters import Filter

from tgbot.config import Config


class AllowedGroupsFilter(Filter):
    async def __call__(self, message: types.Message, config: Config) -> bool | None:
        if message.chat.id in config.tg_bot.group_ids:
            return True
