from typing import Any

from fastapi import FastAPI
from loguru import logger
# from pydantic.dataclasses import dataclass
from .FastapiGatewayAutoGenerageException import FastapiGatewayAutoGenerageException


class Config:
    def __init__(
        self,
        fast_api_app: FastAPI,
        db_settings: dict[str, str | int],
        services_url: list[str],
        service_management: bool = True
    ) -> None:
        self.fast_api_app: FastAPI = fast_api_app
        self.db_settings: dict[str, Any] = db_settings
        self.service_management: bool = service_management
        self.services_url: list[str] = services_url

        self.__validation_parameters()

    def __validation_parameters(self) -> None:
        logger.debug("Validation config parameters")
        self.__validation_db_settings()

    def __validation_db_settings(self) -> None:

        params: dict[str, Any] = {
            "db_host": None,
            "db_port": 3306,
            "db_database": None,
            "db_username": None,
            "db_password": None
        }

        for key, _ in self.db_settings.items():
            if not key in params.keys():
                raise FastapiGatewayAutoGenerageException(
                    f"There is no such key {key}")

        for key, value in params.items():
            if self.db_settings.get(key) is None and value is None:
                raise FastapiGatewayAutoGenerageException(
                    f"No key found {key}")
            else:
                if self.db_settings.get(key) is None:
                    self.db_settings[key] = value
