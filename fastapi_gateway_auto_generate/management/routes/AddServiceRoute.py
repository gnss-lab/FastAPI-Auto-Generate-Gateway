from fastapi_gateway_auto_generate.database import AddService as add_service_database
from fastapi import APIRouter, Depends
from ..models import AddService

from loguru import logger
from ...Config import Config

add_service_router: APIRouter = APIRouter()


class AddServiceRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()
        self.__dependencies = []

        if not self.__config.jwt is None:
            self.__dependencies.append(Depends(self.__config.jwt(self.__config.service_name, "/service")))

        @self.route.post("/service", tags=["Service management"],
                         dependencies=self.__dependencies)
        async def add_service(add_service: AddService) -> bool:
            result = add_service_database(db_url=self.__config.db_url).add_service(
                add_service_model=add_service)
            return result
