from loguru import logger
from fastapi import FastAPI
from .routes import *
from ..Config import Config
from fastapi import Depends


class Management():

    def __init__(self, config: Config) -> None:
        self.config = config
        # logger.debug(str(self.__config))
        self.__app: FastAPI = config.fast_api_app
        logger.debug(self.__app)

        self.__init_routes()

    def __init_routes(self):
        self.__app.include_router(
            router=AddServiceRoute(config=self.config).route)
        self.__app.include_router(
            router=DeleteServiceRoute(config=self.config).route)
        self.__app.include_router(
            router=GetAllInfoServicesRoute(config=self.config).route)
        self.__app.include_router(
            router=RefreshServicesRoute(config=self.config).route)
        logger.debug("Init routes")
