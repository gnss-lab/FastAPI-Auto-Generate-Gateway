import os
import sys
from loguru import logger
from alembic import command
from alembic.config import Config as alembic_config


class InitDatabaseUsecase:
    """The usecase for initializing and verifying database migrations.
    """

    def __init__(self) -> None:
        pass

    def execute(self, db_path:str, db_url: str) -> None:
        """Launch execution of usecase
        Args:
            db_url (str): The path to the SQLite database.
        """
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        project_root = os.path.dirname(
            sys.modules['fastapi_gateway_auto_generate'].__file__)

        logger.debug(project_root)

        alembic_cfg = alembic_config(f"{project_root}/alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        logger.debug(db_url)
        command.upgrade(alembic_cfg, "head")
