from ..models import RouteModel
from types import FunctionType
from fastapi_gateway import route
from .UpdateOpenApiSchemaUsecase import UpdateOpenApiSchemaUsecase
from .DeleteTmpModelsFilesUsecase import DeleteTmpModelsFilesUsecase
from fastapi import FastAPI
from makefun import create_function
from loguru import logger
import fastapi
from typing import Any
import importlib
import os
import sys
from pathlib import Path
import fastapi_gateway_auto_generate


class BuildRoutesUsecase:
    def __init__(self) -> None:
        self.models_routes_vars = {}
        self.models_routes = {}

    def execute(self, services_result: list[dict[str, Any]], fast_api_app: FastAPI) -> None:

        for service_result in services_result:
            for route_model in service_result["route_models"]:

                # print(
                #     exec(f"tmp.models.{service_result['models']}.ConversionParams()"))

                # exit()

                # logger.debug(route_model)

                _import: str = self.__import_model(
                    service_model_name=service_result['models'])

                func, body_list = self.__factory_func(
                    route_model=route_model, _import=_import)

                route(
                    request_method=route_model.request_method,
                    gateway_path=route_model.gateway_path,
                    service_url=route_model.service_url,
                    service_path=route_model.service_path,
                    query_params=route_model.query_params,
                    form_params=route_model.form_params,
                    tags=route_model.tags,
                    body_params=body_list,
                    dependencies=route_model.dependencies,
                )(f=func)

            UpdateOpenApiSchemaUsecase().execute(fast_api_app=fast_api_app)

        DeleteTmpModelsFilesUsecase().execute()

    def __import_model(self, service_model_name: str) -> str:
        _import: str = f"fastapi_gateway_auto_generate.tmp.models.{service_model_name}"
        importlib.import_module(_import)

        return _import

    def __factory_func(self, route_model: RouteModel, _import: str) -> FunctionType:

        def func_impl(*args, **kwargs):
            pass

        arguments: list[dict[str, str]] = []

        queries = ""
        files = ""

        body_list = []

        # Body
        if not route_model.body_params is None:
            for i, body in enumerate(route_model.body_params):

                argument = {}
                argument["name"] = body + f"{i}"
                argument["type"] = f"{_import}.{body}"

                # if not route_model.query_required[i]:
                #     argument["value"] = "None"
                #     argument["type"] = "str | None"

                # if route_model.query_is_cookie[i]:
                #     argument["value"] = "fastapi.Cookie(default=None)"

                body_list.append(body + f"{i}")
                arguments.append(argument)

        # Queries
        if not route_model.query_params is None:
            for i, query in enumerate(route_model.query_params):

                argument = {}
                argument["name"] = query
                argument["type"] = "str"

                if not route_model.query_required[i]:
                    argument["value"] = "None"
                    argument["type"] = "str | None"

                if route_model.query_is_cookie[i]:
                    argument["value"] = "fastapi.Cookie(default=None)"

                arguments.append(argument)

        # Files
        if not route_model.form_params is None:
            for file in route_model.form_params:
                argument = {}
                argument["name"] = file
                argument["type"] = "fastapi.UploadFile"
                argument["value"] = "fastapi.File()"
                arguments.append(argument)

        func_sig: str = "func(request: fastapi.Request, response: fastapi.Response, "
        for argument in arguments:
            func_sig += f"{argument['name']}: {argument['type']}"

            if not argument.get("value") is None:
                func_sig += f" = {argument['value']}, "
            else:
                func_sig += ", "

        func_sig += ")"

        # Cookie

        logger.debug(func_sig)

        test = create_function(func_sig, func_impl)

        # exit()
        return test, body_list
