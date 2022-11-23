from alembic.config import Config as alembic_config
from alembic import command
from loguru import logger


class InitDatabaseUsecase:
    def __init__(self) -> None:
        pass

    def execute(self, db_url: str) -> None:
        alembic_cfg = alembic_config("./alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        logger.debug(db_url)
        command.upgrade(alembic_cfg, "head")
