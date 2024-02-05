from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    token: str
    group_ids: list[int]

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        group_ids = env.list("GROUP_IDS", subcast=int)
        return TgBot(token=token, group_ids=group_ids)


@dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str] = "redis_cache"

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD", default=None)
        redis_port = env.int("REDIS_PORT", default=6379)
        return RedisConfig(redis_pass=redis_pass, redis_port=redis_port)


@dataclass
class Mistral:
    token: str

    @staticmethod
    def from_env(env: Env):
        token = env.str("MISTRAL_TOKEN")
        return Mistral(token=token)


@dataclass
class Config:
    tg_bot: TgBot
    mistral: Mistral
    redis: RedisConfig


BOT_ADMINS_STORAGE_KEY = "spam:bot_admins"


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        mistral=Mistral.from_env(env),
        redis=RedisConfig.from_env(env),
    )
