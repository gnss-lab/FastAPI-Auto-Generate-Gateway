import re

import requests
# import validators
from typing import List
from pathlib import Path
from loguru import logger
from pprint import pprint
from fastapi import FastAPI
from requests import Response
from types import FunctionType
from fastapi_gateway import route
from .RouteModel import RouteModel
from .OpenApiParser import OpenApiParser
from datamodel_code_generator import InputFileType, generate
# from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi

from .management import Management


class FastapiGatewayAutoGenerate:
    def __init__(self, fast_api_app: FastAPI, services_url: list[str], management: bool = True) -> None:

        self.__fast_api_app: FastAPI = fast_api_app
        self.__services_url: list[str] = services_url

        if management:
            self.__init_management_urls()

        self.__routes_model: List[RouteModel] = []

        self.__open_api_parser = OpenApiParser()

        self.models_routes_vars = None
        self.models_routes: None = None

    def __init_management_urls(self):
        m: Management = Management(app=self.__fast_api_app)

    def init_database(self):
        pass

    def __update_openapi_schema(self):
        self.__fast_api_app.openapi_schema = None
        self.__fast_api_app.openapi()

    def build_routes(self) -> None:
        for service_url in self.__services_url:

            # if validators.url(service_url):
            #     pass

            self.__open_api_parser.parse_from_service(url=service_url)

            for path in self.__open_api_parser.get_paths():

                if self.__open_api_parser.check_auto_generate_in_api_gateway(path=path):

                    path_method: str = self.__open_api_parser.get_path_method(
                        path)

                    route_model: RouteModel = RouteModel(
                        request_method=getattr(
                            self.__fast_api_app, path_method),
                        gateway_path=path,
                        service_url=service_url,
                        service_path=path
                    )

                    route_model.query_params, route_model.query_required = self.__open_api_parser.get_queries_param(
                        path=path, method=path_method)

                    route_model.form_params = self.__open_api_parser.get_body_multipart_form_data(
                        path=path, method=path_method)

                    self.__routes_model.append(route_model)
                else:
                    continue

            self.models_routes_vars, self.models_routes = self.__generate_models()

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

        self.__update_openapi_schema()

    def __generate_models(self):

        temporary_directory = Path(
            Path.home() / "Documents/xitowzys/ISZF/fastapi-gateway-auto-generate")

        output = Path(temporary_directory / 'tmp/model.py')
        input = Path(temporary_directory / "tests/data/swagger.json")

        generate(
            input_=self.__open_api_parser.get_raw_resoponse_in_string(),
            input_file_type=InputFileType.OpenAPI,
            input_filename="example.json",
            output=output
        )

        vars = {}
        model: str = output.read_text()
        classes: list[str] = re.findall(r"class\s([A-Za-z0-91]*)", model)

        exec(model, vars)
        output.unlink()

        return vars, classes
