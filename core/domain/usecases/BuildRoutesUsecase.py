from ..models import RouteModel
from types import FunctionType
from fastapi_gateway import route
from .UpdateOpenApiSchemaUsecase import UpdateOpenApiSchemaUsecase
from fastapi import FastAPI


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
