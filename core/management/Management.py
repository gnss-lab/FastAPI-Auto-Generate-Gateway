from loguru import logger
from fastapi import FastAPI
from .routes import *


class Management():

    def __init__(self, app: FastAPI) -> None:
        self.__app: FastAPI = app
        logger.debug("Management run")

        self.__init_routes()

    def __init_routes(self):
        self.__app.include_router(router=add_service_router)
        self.__app.include_router(router=delete_service_router)
        self.__app.include_router(router=get_all_info_services_router)
        self.__app.include_router(router=refresh_services_router)
        logger.debug("Init routes")
