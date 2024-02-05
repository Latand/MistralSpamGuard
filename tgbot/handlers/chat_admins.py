import json

from aiogram import Router, types
from aiogram.filters.chat_member_updated import (
    ADMINISTRATOR,
    KICKED,
    LEFT,
    MEMBER,
    PROMOTED_TRANSITION,
    RESTRICTED,
    ChatMemberUpdatedFilter,
)
from aiogram.fsm.storage.redis import RedisStorage

from tgbot.config import BOT_ADMINS_STORAGE_KEY
from tgbot.filters.groups_filter import AllowedGroupsFilter

chat_admins_router = Router()

DEMOTED_TRANSITION = ADMINISTRATOR >> (MEMBER | RESTRICTED | LEFT | KICKED)


@chat_admins_router.chat_member(
    ChatMemberUpdatedFilter(PROMOTED_TRANSITION), AllowedGroupsFilter()
)
async def chat_admin_promoted(
    chat_member_updated: types.ChatMemberUpdated, storage: RedisStorage
):
    result = await storage.redis.get(BOT_ADMINS_STORAGE_KEY)
    if not result:
        bot_admins = [
            admin.user.id
            for admin in await chat_member_updated.chat.get_administrators()
        ]
    else:
        bot_admins = json.loads(result)
        bot_admins.append(chat_member_updated.new_chat_member.user.id)
    await storage.redis.set(BOT_ADMINS_STORAGE_KEY, json.dumps(bot_admins))


@chat_admins_router.chat_member(
    ChatMemberUpdatedFilter(DEMOTED_TRANSITION), AllowedGroupsFilter()
)
async def chat_admin_demoted(
    chat_member_updated: types.ChatMemberUpdated, storage: RedisStorage
):
    result = await storage.redis.get(BOT_ADMINS_STORAGE_KEY)
    if not result:
        bot_admins = [
            admin.user.id
            for admin in await chat_member_updated.chat.get_administrators()
        ]
    else:
        bot_admins: list = json.loads(result)
        try:
            bot_admins.remove(chat_member_updated.new_chat_member.user.id)
        except ValueError:
            return
    await storage.redis.set(BOT_ADMINS_STORAGE_KEY, json.dumps(bot_admins))
