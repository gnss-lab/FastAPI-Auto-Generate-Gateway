from fastapi import APIRouter,  Request
from ...Config import Config
from loguru import logger
from core.domain.usecases import RefreshServicesUsecase


class RefreshServicesRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()

        @self.route.patch("/services", tags=["Service management"])
        async def refresh_services(request: Request) -> bool:
            RefreshServicesUsecase().execute(config=self.__config)
            return True
