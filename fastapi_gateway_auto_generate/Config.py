import os
from typing import Optional, Callable, Type, TypeVar
from fastapi import FastAPI
from fastapi_gateway_auto_generate.exceptions import ConfigException
from loguru import logger

from .utils.RichTraceback import RichTraceback

T = TypeVar('T')


class Config:
    """The Configuration class is intended for configuring the auto-generation of services for the API Gateway.
    Args:
        fast_api_app (FastAPI): Pointer to your FastAPI application.
        service_management (bool): Enable the built-in service manager.
        db_path (str): The path to the SQLite database.
        jwt (Optional[Type[T]]): The class responsible for protecting the routers.
        celery_app (Optional[Celery]): The Celery object responsible for transferring large files.
    """

    def __init__(
            self,
            fast_api_app: FastAPI,
            service_management: bool = True,
            db_path: str = "./",
            db_name: str = "database",
            jwt: Optional[Type[T]] = None,
            allow_large_files: bool = False,
            broker_url: str = ""
    ) -> None:
        self.fast_api_app: FastAPI = fast_api_app
        self.service_management: bool = service_management
        self.jwt = jwt
        self.service_name = "API-Gateway"

        if db_name != "database":
            self.db_name = db_name
        else:
            self.db_name = "database"

        if db_path != "./":
            self.db_path = db_path
        else:
            self.db_path = "./"

        # self.db_path = "./database.db" if db_path is None else db_path
        self.db_url = f"sqlite:///{self.get_database_absolute_path()}"

        # try:
        #     if not (allow_large_files and broker_url):
        #         raise ConfigException("Broker URL was not specified")
        # except Exception as e:
        #     RichTraceback().console_call_exception()

        self.allow_large_files: bool = allow_large_files

        # self.__validation_parameters()

    def get_database_absolute_path(self):
        return f"{os.path.abspath(self.db_path)}/{self.db_name}.db"
    # def __validation_parameters(self) -> None:
    #     """_summary_
    #     """
    #     logger.debug("Validation config parameters")
