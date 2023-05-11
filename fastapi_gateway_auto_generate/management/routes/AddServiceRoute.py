from typing import Dict

from fastapi_gateway_auto_generate.database import AddService as add_service_database
from fastapi import APIRouter, Depends, HTTPException
from ..models import AddService

from loguru import logger
from ...Config import Config
from ...utils import success_code

add_service_router: APIRouter = APIRouter()


class AddServiceRoute:
    """Router for adding a service
        Args:
            config (Config): The Config object with its configuration.

        Returns:
            result (bool): True if the addition was successful, otherwise False.
    """

    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()
        self.__dependencies = []

        if not self.__config.jwt is None:
            self.__dependencies.append(Depends(self.__config.jwt(self.__config.service_name, "/service", "post")))

        @self.route.post("/service", tags=["Service management"],
                         dependencies=self.__dependencies)
        async def add_service(add_service: AddService) -> dict[str, dict[str, str | int]]:
            result, err = add_service_database(db_url=self.__config.db_url).add_service(
                add_service_model=add_service)

            if err:
                raise HTTPException(status_code=409, detail=err)

            return success_code(msg="The service has been added")
