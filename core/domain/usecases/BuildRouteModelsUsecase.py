# from loguru import logger
from ...utils.OpenApiParser import OpenApiParser
from ..models import RouteModel
from fastapi import FastAPI
from core.database import GetAllServices, StatusService
from ...Config import Config
from loguru import logger
from core.management.models import GetAllInfoServices


class BuildRouteModelsUsecase:
    def __init__(self) -> None:
        self.__open_api_parser: OpenApiParser = OpenApiParser()

    def execute(self, config: Config) -> list[RouteModel]:

        routes_model: list[RouteModel] = []

        get_all_info_services_model: GetAllInfoServices = GetAllInfoServices(
            page=1)

        services, err = GetAllServices(db_url=config.db_url).get_all_services(
            get_all_info_services_model=get_all_info_services_model)

        if not err is None:
            return routes_model

        count_page: int = services["metadata"]["count_page"]

        StatusService(db_url=config.db_url).delete_all_rows()

        if err is None:
            for _ in range(0, count_page):

                services, err = GetAllServices(db_url=config.db_url).get_all_services(
                    get_all_info_services_model=get_all_info_services_model)

                for service in services["services"]:

                    # if validators.url(service_url):
                    #     pass

                    url = f"{service['domain']}:{service['port']}"

                    logger.debug(url)

                    err, status_code = self.__open_api_parser.parse_from_service(
                        url=url)

                    logger.debug(status_code)

                    StatusService(db_url=config.db_url).set_status_service(
                        id_service=service["id"],
                        status_code=status_code
                    )

                    if err:
                        continue

                    for path in self.__open_api_parser.get_paths():

                        if self.__open_api_parser.check_auto_generate_in_api_gateway(path=path):

                            path_method: str = self.__open_api_parser.get_path_method(
                                path)

                            route_model: RouteModel = RouteModel(
                                request_method=getattr(
                                    config.fast_api_app, path_method),
                                gateway_path=f"/{service['name']}{path}",
                                service_url=url,
                                service_path=path
                            )

                            route_model.query_params, route_model.query_required = self.__open_api_parser.get_queries_param(
                                path=path, method=path_method)

                            route_model.form_params = self.__open_api_parser.get_body_multipart_form_data(
                                path=path, method=path_method)

                            routes_model.append(route_model)
                        else:
                            continue

                get_all_info_services_model.page += 1

        logger.debug(routes_model)
        return routes_model
