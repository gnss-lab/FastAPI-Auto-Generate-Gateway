from fastapi import APIRouter, Request, Depends
from ...Config import Config
from loguru import logger
from fastapi_gateway_auto_generate.domain.usecases import RefreshServicesUsecase


class RefreshServicesRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()
        self.__dependencies = []

        if not self.__config.jwt is None:
            self.__dependencies.append(Depends(self.__config.jwt(self.__config.service_name, "/services", "patch")))

        @self.route.patch("/services", tags=["Service management"],
                         dependencies=self.__dependencies)
        async def refresh_services(request: Request) -> bool:
            RefreshServicesUsecase().execute(config=self.__config)
            return True
