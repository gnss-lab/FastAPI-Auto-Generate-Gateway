import os
import sys
from loguru import logger
from alembic import command
from alembic.config import Config as alembic_config


class InitDatabaseUsecase:
    def __init__(self) -> None:
        pass

    def execute(self, db_url: str) -> None:
        project_root = os.path.dirname(
            sys.modules['fastapi_gateway_auto_generate'].__file__)

        logger.debug(project_root)

        alembic_cfg = alembic_config(f"{project_root}/alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        logger.debug(db_url)
        command.upgrade(alembic_cfg, "head")
