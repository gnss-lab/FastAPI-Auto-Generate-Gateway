import importlib
from types import FunctionType
from typing import Any, Tuple

from fastapi import FastAPI
from fastapi_gateway import route
from loguru import logger
from makefun import create_function

from .DeleteTmpModelsFilesUsecase import DeleteTmpModelsFilesUsecase
from .UpdateOpenApiSchemaUsecase import UpdateOpenApiSchemaUsecase
from ..models import RouteModel
from ... import Config


class BuildRoutesUsecase:
    def __init__(self, config: Config) -> None:
        self.models_routes_vars = {}
        self.models_routes = {}
        self.__config: Config = config

    def execute(self, services_result: list[dict[str, Any]], fast_api_app: FastAPI) -> None:

        for service_result in services_result:
            for route_model in service_result["route_models"]:
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

    def __factory_func(self, route_model: RouteModel, _import: str) -> Tuple[FunctionType, list[str]]:

        func_impl = None

        def func_impl(*args, **kwargs):
            pass
        #
        #     # Определяем тело функции
        # if self.__config.celery_app is not None:
        #         def func_impl2(a, b):
        #             pass
        #     else:
        #         def func_impl3(*args, **kwargs):
        #             pass

        arguments: list[dict[str, str | None]] = []
        body_list: list[str] = []

        # Body parameters
        if route_model.body_params is not None:
            for i, body in enumerate(route_model.body_params):
                argument = {
                    "name": f"{body}{i}",
                    "type": f"{_import}.{body}"
                }
                body_list.append(f"{body}{i}")
                arguments.append(argument)

        # Query parameters
        if route_model.query_params is not None:
            for i, query in enumerate(route_model.query_params):
                argument = {
                    "name": query,
                    "type": "str"
                }
                if not route_model.query_required[i]:
                    argument["value"] = "None"
                    argument["type"] = "str | None"
                if route_model.query_is_cookie[i]:
                    argument["value"] = "fastapi.Cookie(default=None)"
                arguments.append(argument)

        # Files
        if route_model.form_params is not None:
            for file in route_model.form_params:
                argument = {
                    "name": file,
                    "type": "fastapi.UploadFile",
                    "value": "fastapi.File()"
                }



                arguments.append(argument)

        # Construct the function signature
        func_sig: str = "func(request: fastapi.Request, response: fastapi.Response, "
        for argument in arguments:
            func_sig += f"{argument['name']}: {argument['type']}"

            if "value" in argument:
                func_sig += f" = {argument['value']}, "
            else:
                func_sig += ", "

        func_sig += ")"
        logger.debug(func_sig)

        # Create the function
        func: FunctionType = create_function(func_sig, func_impl)

        return func, body_list
