# pyright: strict

from typing import Literal

from pydantic import BaseSettings


class _Settings(BaseSettings):
    env: Literal["production", "development", "testing", "local"] = "local"
    """環境名"""

    debug: bool = False
    """デバッグモードかどうか"""


settings = _Settings()
