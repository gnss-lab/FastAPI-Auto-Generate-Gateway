from ..models import RouteModel
from types import FunctionType
from fastapi_gateway import route
from .UpdateOpenApiSchemaUsecase import UpdateOpenApiSchemaUsecase
from fastapi import FastAPI
from makefun import create_function
from loguru import logger
import fastapi


class BuildRoutesUsecase:
    def __init__(self) -> None:
        self.models_routes_vars = {}
        self.models_routes = {}

    def execute(self, route_model_list: list[RouteModel], fast_api_app: FastAPI) -> None:
        for route_model in route_model_list:
            # logger.debug(route_model)
            func: FunctionType = self.__factory_func(route_model=route_model)

            route(
                request_method=route_model.request_method,
                gateway_path=route_model.gateway_path,
                service_url=route_model.service_url,
                service_path=route_model.service_path,
                query_params=route_model.query_params,
                form_params=route_model.form_params,
                tags=route_model.tags
            )(f=func)

        UpdateOpenApiSchemaUsecase().execute(fast_api_app=fast_api_app)

    def __factory_func(self, route_model: RouteModel) -> FunctionType:

        def func_impl(*args, **kwargs):
            pass

        arguments: list[dict[str, str]] = []

        queries = ""
        files = ""

        # Queries
        if not route_model.query_params is None:
            for i, query in enumerate(route_model.query_params):

                argument = {}
                argument["name"] = query
                argument["type"] = "str"

                if not route_model.query_required[i]:
                    argument["value"] = "None"
                    argument["type"] = "str | None"

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

        test = create_function(func_sig, func_impl)

        logger.debug(func_sig)

        return test
