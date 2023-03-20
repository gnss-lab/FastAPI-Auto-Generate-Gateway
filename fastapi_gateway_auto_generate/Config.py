import os
from typing import Optional, Callable, Type, TypeVar
from fastapi import FastAPI
from fastapi_gateway_auto_generate.exceptions import ConfigException
from loguru import logger

from .utils.RichTraceback import RichTraceback

T = TypeVar('T')


class Config:
    """The configuration class is intended for configuring auto-generat ion of services for the API Gateway.
    Args:
        fast_api_app (FastAPI): Pointer to your FastAPI application.
        service_management (bool): Enable the built-in service manager.
    """

    def __init__(
            self,
            fast_api_app: FastAPI,
            service_management: bool = True,
            db_path: Optional[str] = None,
            jwt: Optional[Type[T]] = None,
            allow_large_files: bool = False,
            broker_url: str = ""
    ) -> None:
        self.fast_api_app: FastAPI = fast_api_app
        self.service_management: bool = service_management
        self.jwt = jwt
        self.service_name = "API-Gateway"

        self.db_path = "./database.db" if db_path is None else db_path
        self.db_url = f"sqlite:///{os.path.abspath(self.db_path)}"

        # try:
        #     if not (allow_large_files and broker_url):
        #         raise ConfigException("Broker URL was not specified")
        # except Exception as e:
        #     RichTraceback().console_call_exception()

        self.allow_large_files: bool = allow_large_files

        self.__validation_parameters()

    def __validation_parameters(self) -> None:
        """_summary_
        """
        logger.debug("Validation config parameters")
