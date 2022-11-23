# import re

# import requests
# import validators
# from typing import List, Any
# from pathlib import Path
# from loguru import logger
# from pprint import pprint
# from fastapi import FastAPI
# from requests import Response
# from types import FunctionType
# from fastapi_gateway import route
# from .RouteModel import RouteModel
# from .utils.OpenApiParser import OpenApiParser
# from datamodel_code_generator import InputFileType, generate
# from pydantic import BaseModel, Field
# from fastapi.openapi.utils import get_openapi

from .management import Management
from .Config import Config
# import os.path
# from alembic.config import Config as alembic_config
# from alembic import command
from core.domain.usecases import *
# from core.domain.models import RouteModel


class AutoGenerate:

    def __init__(self, config: Config) -> None:
        self.__config = config

        InitDatabaseUsecase().execute(db_url=config.db_url)

        if self.__config.service_management:
            self.__init_management_urls()

        # self.__routes_model: List[RouteModel] = []

        # self.__open_api_parser = OpenApiParser()

        # self.models_routes_vars = {}
        # self.models_routes: None = {}

        self.services_url = ["http://127.0.0.1:7200"]

        self.build()

    def __init_management_urls(self):
        m: Management = Management(config=self.__config)

    def build(self) -> None:
        routes_model = BuildRouteModelsUsecase().execute(
            services_url=self.services_url,
            fast_api_app=self.__config.fast_api_app
        )

        # logger.debug(self.__routes_model)

        # self.models_routes_vars, self.models_routes = self.__generate_models()

        BuildRoutesUsecase().execute(
            route_model_list=routes_model,
            fast_api_app=self.__config.fast_api_app
        )

    # def __generate_models(self):

    #     temporary_directory = Path(
    #         Path.home() / "Documents/xitowzys/ISZF/fastapi-gateway-auto-generate")

    #     output = Path(temporary_directory / 'tmp/model.py')
    #     input = Path(temporary_directory / "tests/data/swagger.json")

    #     generate(
    #         input_=self.__open_api_parser.get_raw_resoponse_in_string(),
    #         input_file_type=InputFileType.OpenAPI,
    #         input_filename="example.json",
    #         output=output
    #     )

    #     vars = {}
    #     model: str = output.read_text()
    #     classes: list[str] = re.findall(r"class\s([A-Za-z0-91]*)", model)

    #     exec(model, vars)
    #     output.unlink()

    #     return vars, classes
