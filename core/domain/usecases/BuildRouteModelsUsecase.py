# from loguru import logger
from ...utils.OpenApiParser import OpenApiParser
from ..models import RouteModel
from fastapi import FastAPI


class BuildRouteModelsUsecase:
    def __init__(self) -> None:
        self.__open_api_parser: OpenApiParser = OpenApiParser()

    def execute(self, services_url: list[str], fast_api_app: FastAPI) -> list[RouteModel]:

        routes_model: list[RouteModel] = []

        for service_url in services_url:

            # if validators.url(service_url):
            #     pass

            self.__open_api_parser.parse_from_service(url=service_url)

            for path in self.__open_api_parser.get_paths():

                if self.__open_api_parser.check_auto_generate_in_api_gateway(path=path):

                    path_method: str = self.__open_api_parser.get_path_method(
                        path)

                    route_model: RouteModel = RouteModel(
                        request_method=getattr(fast_api_app, path_method),
                        gateway_path=path,
                        service_url=service_url,
                        service_path=path
                    )

                    route_model.query_params, route_model.query_required = self.__open_api_parser.get_queries_param(
                        path=path, method=path_method)

                    route_model.form_params = self.__open_api_parser.get_body_multipart_form_data(
                        path=path, method=path_method)

                    routes_model.append(route_model)
                else:
                    continue

        return routes_model
