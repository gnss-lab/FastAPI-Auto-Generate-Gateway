import re

import requests
# import validators
from typing import List, Any
from pathlib import Path
from loguru import logger
from pprint import pprint
from fastapi import FastAPI
from requests import Response
from types import FunctionType
from fastapi_gateway import route
# from .RouteModel import RouteModel
from .utils.OpenApiParser import OpenApiParser
from datamodel_code_generator import InputFileType, generate
# from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi

from .management import Management
from .Config import Config
import os.path
from alembic.config import Config as alembic_config
from alembic import command
from core.domain.usecases import *
from core.domain.models import RouteModel


class AutoGenerate:

    def __init__(self, config: Config) -> None:
        self.__config = config

        InitDatabaseUsecase().execute(db_url=config.db_url)

        if self.__config.service_management:
            self.__init_management_urls()

        self.__routes_model: List[RouteModel] = []

        # self.__open_api_parser = OpenApiParser()

        self.models_routes_vars = {}
        self.models_routes: None = {}

        self.services_url = ["http://127.0.0.1:8000"]

        self.build()

    def __init_management_urls(self):
        m: Management = Management(config=self.__config)

    def build(self) -> None:
        self.__routes_model = BuildRoutesUsecase().execute(
            services_url=self.services_url,
            fast_api_app=self.__config.fast_api_app
        )

        logger.debug(self.__routes_model)

        # self.models_routes_vars, self.models_routes = self.__generate_models()

        self.__init_functions()

    def __factory_func(self, route_model: RouteModel) -> FunctionType:
        vars: dict[str, function] = {}

        import_fast_api: str = "import fastapi\n"

        queries = ""
        files = ""

        # Queries
        if not route_model.query_params is None:
            for query in route_model.query_params:

                if query in route_model.query_params[-1]:
                    queries = queries + \
                        f"{query}: str,"
                else:
                    queries = queries + f"{query}: str,"

        # Files
        if not route_model.form_params is None:
            for file in route_model.form_params:
                if file in route_model.form_params[-1]:
                    files = files + \
                        f"{file}: fastapi.UploadFile = fastapi.File(),"
                else:
                    files = files + \
                        f"{file}: fastapi.UploadFile = fastapi.File(),"

        # Forms
        # -

        result: str = f"{import_fast_api}\n\ndef func(request: fastapi.Request, response: fastapi.Response, {queries if not None else ''} {files if not None else ''}):\n\tpass"

        exec(result, self.models_routes_vars)

        return self.models_routes_vars["func"]

    def __init_functions(self) -> None:

        for route_model in self.__routes_model:
            # logger.debug(route_model)
            func: FunctionType = self.__factory_func(route_model=route_model)

            route(
                request_method=route_model.request_method,
                gateway_path=route_model.gateway_path,
                service_url=route_model.service_url,
                service_path=route_model.service_path,
                query_params=route_model.query_params,
                form_params=route_model.form_params,
                tags=["ok"]
            )(f=func)

        UpdateOpenApiSchemaUsecase().execute(fast_api_app=self.__config.fast_api_app)

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
