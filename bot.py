import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from mistralai.async_client import MistralAsyncClient

from tgbot.config import load_config
from tgbot.handlers import routers_list


def setup_logging():
    log_level = logging.INFO
    # bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    # logger = logging.getLogger(__name__)
    logging.info("Starting bot")


async def main():
    setup_logging()

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = RedisStorage.from_url(
        config.redis.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )
    dp = Dispatcher(storage=storage)
    mistral_client = MistralAsyncClient(api_key=config.mistral.token)

    dp.workflow_data.update(
        mistral_client=mistral_client,
        storage=storage,
        config=config,
    )
    dp.include_routers(*routers_list)
    logging.info("Bot started!")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
