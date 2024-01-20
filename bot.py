import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from mistralai.async_client import MistralAsyncClient
from tgbot.config import load_config
from tgbot.handlers import routers_list


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    mistral_client = MistralAsyncClient(api_key=config.mistral.token)

    dp.workflow_data.update(
        mistral_client=mistral_client,
    )
    dp.include_routers(*routers_list)
    print("Bot started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
