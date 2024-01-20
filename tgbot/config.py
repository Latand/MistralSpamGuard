from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        return TgBot(token=token)


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


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        mistral=Mistral.from_env(env),
    )
