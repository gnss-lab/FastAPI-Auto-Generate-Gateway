import os
from typing import Optional
from fastapi import FastAPI
from .GeneratorException import FastapiGatewayAutoGenerageException
from loguru import logger


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
        jwt = None
    ) -> None:
        self.fast_api_app: FastAPI = fast_api_app
        self.service_management: bool = service_management
        self.jwt = jwt

        if db_path is None:
            self.db_path: str = "./database.db"
            self.db_url: str = "sqlite:///database.db"
            # os.environ["SQLITE_DRIVER_PATH"] = "sqlite:///" + \
            #     os.path.abspath(self.db_path)
        else:
            self.db_path: str = db_path
            self.db_url: str = "sqlite:///" + os.path.abspath(db_path)
            # os.environ["SQLITE_DRIVER_PATH"] = "sqlite:///" + \
            #     os.path.abspath(self.__config.db_path)

        self.__validation_parameters()

    def __validation_parameters(self) -> None:
        """_summary_
        """
        logger.debug("Validation config parameters")
