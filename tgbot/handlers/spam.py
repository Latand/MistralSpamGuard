from aiogram import F, Router
from aiogram.types import ChatPermissions, Message

from tgbot.filters.spam_detection import SpamFilter

spam_router = Router()


@spam_router.message(F.chat.id == -1001041869725, SpamFilter())
async def spam_handler(message: Message):
    await message.chat.restrict(
        user_id=message.from_user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
        ),
    )
    # message that user has been restricted
    await message.answer(
        f"User {message.from_user.full_name} has been restricted for spamming. Write to admins if you think it's a mistake."
    )
    await message.delete()
