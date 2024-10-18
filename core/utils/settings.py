from environs import Env
from dataclasses import dataclass
from typing import List


@dataclass
class Settings:
    api_path: str
    terminal_ips: List[str]


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        api_path=env.str('API_PATH'),
        terminal_ips=env.list('TERMINAL_IPS'),
    )


settings = get_settings('.env')
