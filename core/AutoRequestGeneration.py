import json

# import string
import requests
import validators
from loguru import logger
from pprint import pprint
from fastapi import FastAPI
from requests import Response
from .RouteModel import RouteModel
from fastapi_gateway import route
from typing import List, Any
from types import FunctionType
from .OpenApiParser import OpenApiParser


class AutoRequestGeneration:
    def __init__(self, fast_api_app: FastAPI, services_url: list[str]) -> None:

        self.__fast_api_app: FastAPI = fast_api_app

        self.__routes_model: List[RouteModel] = []
        self.__services_url: list[str] = services_url

        self.__open_api_parser = OpenApiParser()

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

            # pprint(self.__routes_model)
        self.__init_functions()

    def __factory_func(self, route_model: RouteModel) -> FunctionType:
        vars: dict[str, function] = {}

        import_fast_api: str = "import fastapi\n"

        queries = ""

        if not route_model.query_params is None:
            for query in route_model.query_params:
                print(query)

                if query in route_model.query_params[-1]:
                    queries = queries + f"{query}: str"
                else:
                    queries = queries + f"{query}: str,"

        else:
            pass

        exec(f"{import_fast_api}\n\ndef func(request: fastapi.Request, response: fastapi.Response, {queries}):\n\tpass", vars)

        return vars["func"]

    def __init_functions(self) -> None:

        for route_model in self.__routes_model:
            func: FunctionType = self.__factory_func(route_model=route_model)

            route(

                request_method=route_model.request_method,
                gateway_path=route_model.gateway_path,
                service_url=route_model.service_url,
                service_path=route_model.service_path,
                query_params=route_model.query_params,
                form_params=route_model.form_params,

                # response_model_include=
                include_in_schema=True,
                # response_model_include={"Body_generate_map_mosgim_generate_map_post": {
                #     "title": "Body_generate_map_mosgim_generate_map_post",
                #     "required": [
                #         "file"
                #     ],
                #     "type": "object",
                #     "properties": {
                #         "file": {
                #             "title": "File",
                #             "type": "string",
                #             "format": "binary"
                #         }
                #     }
                # }}
            )(f=func)
