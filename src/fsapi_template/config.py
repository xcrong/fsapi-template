import logging
from typing import Literal

import click
import toml
from pydantic_settings import BaseSettings, SettingsConfigDict

with open("pyproject.toml", encoding="utf-8") as f:
    pyproject = toml.load(f)
    pj_name: str = pyproject["project"]["name"]


class AppConfig(BaseSettings):
    api_key: str = ""

    model_config = SettingsConfigDict(env_file=".envs", extra="ignore")


class UvicornConfig(BaseSettings):
    app: str = f"{pj_name}:app".replace("-", "_")
    host: str = "127.0.0.1"
    port: int = 8001
    reload: bool = False
    # if reload is True
    reload_includes: list[str] = ["**/*.py", ".envs"]
    log_level: Literal[
        "critical", "error", "warning", "info", "debug", "trace"
    ] = "info"

    model_config = SettingsConfigDict(env_file=".envs", extra="ignore")


class CustomLogger:
    def __init__(self, name, level=logging.DEBUG):
        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 创建控制台处理器并设置级别
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        self.logger.addHandler(console_handler)

        # 定义日志级别颜色
        self.colors = {
            "DEBUG": click.style("DEBUG", fg="cyan"),
            "INFO": click.style("INFO", fg="green"),
            "WARNING": click.style("WARNING", fg="yellow"),
            "ERROR": click.style("ERROR", fg="red"),
            "CRITICAL": click.style("CRITICAL", fg="bright_red"),
        }

    def debug(self, message):  # pragma: no cover
        self.logger.debug(f"{self.colors['DEBUG']}:     {message}")

    def info(self, message):  # pragma: no cover
        self.logger.info(f"{self.colors['INFO']}:     {message}")

    def warning(self, message):  # pragma: no cover
        self.logger.warning(f"{self.colors['WARNING']}:     {message}")

    def error(self, message):  # pragma: no cover
        self.logger.error(f"{self.colors['ERROR']}:     {message}")

    def critical(self, message):  # pragma: no cover
        self.logger.critical(f"{self.colors['CRITICAL']}:     {message}")


app_config = AppConfig()
uvicorn_config = UvicornConfig()

logger = CustomLogger(name=pj_name)
