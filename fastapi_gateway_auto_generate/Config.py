import os
from typing import Optional
from fastapi import FastAPI
from .GeneratorException import FastapiGatewayAutoGenerageException


class Config:

    def __init__(
        self,
        fast_api_app: FastAPI,
        service_management: bool = True,
        db_path: Optional[str] = None
    ) -> None:
        self.fast_api_app: FastAPI = fast_api_app
        self.service_management: bool = service_management

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
        logger.debug("Validation config parameters")
