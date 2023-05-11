from fastapi_gateway_auto_generate.database import StatusService, UrlService, GetAllServices, DeleteService
from . import *
from ...Config import Config
from loguru import logger
from ..models import RouteModel
from fastapi_gateway_auto_generate.management.models import GetAllInfoServices
from fastapi_gateway_auto_generate.management.models import DeleteService as delete_service_model


class RefreshServicesUsecase:
    """The usecase for updating and verifying all connected services.
    """

    def __init__(self):
        pass

    def execute(self, config: Config) -> None:
        """Launch execution of usecase
        Args:
            config (Config): The Config object with its configuration.
        """

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

                if service['delete']:
                    # print(service['id'])
                    DeleteService(db_url=config.db_url).delete_service(
                        delete_service_model=delete_service_model(id_service=service['id'])
                    )

        services_result = BuildRouteModelsUsecase().execute(
            config=config
        )

        BuildRoutesUsecase().execute(
            services_result=services_result,
            fast_api_app=config.fast_api_app
        )

        logger.success("Services have been successfully updated")
