from fastapi_gateway_auto_generate.database import StatusService, UrlService, GetAllServices
from . import *
from ...Config import Config
from loguru import logger
from ..models import RouteModel
from fastapi_gateway_auto_generate.management.models import GetAllInfoServices


class RefreshServicesUsecase:
    def __init__(self):
        pass

    def execute(self, config: Config) -> None:

        get_all_info_services_model: GetAllInfoServices = GetAllInfoServices(
            page=1)

        services, err = GetAllServices(db_url=config.db_url).get_all_services(
            get_all_info_services_model=get_all_info_services_model)

        if not err is None:
            return None

        count_page: int = services["metadata"]["count_page"]

        routes = config.fast_api_app.router.routes

        for _ in range(0, count_page):
            for service in services["services"]:
                for url in service["urls"]:
                    for i, r in enumerate(routes):
                        if r.path == f"/{service['name']}{url}":
                            del config.fast_api_app.routes[i]
                            logger.debug(r)

        route_model_list: list[RouteModel] = BuildRouteModelsUsecase().execute(
            config=config)

        BuildRoutesUsecase().execute(
            route_model_list=route_model_list,
            fast_api_app=config.fast_api_app
        )

        UpdateOpenApiSchemaUsecase().execute(fast_api_app=config.fast_api_app)

        logger.info("Services have been successfully updated")
