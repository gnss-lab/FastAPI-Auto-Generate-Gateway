import re
import os
import sys
import json
import shortuuid
from typing import Any
from pathlib import Path
from pprint import pprint
from loguru import logger
from fastapi import FastAPI, Depends
from ...Config import Config
from ..models import RouteModel
from fastapi_gateway_auto_generate.utils.APITags import APITags

from fastapi_openapi_parser import OpenApiParser
from fastapi_gateway_auto_generate.management.models import GetAllInfoServices
from datamodel_code_generator import InputFileType, generate
from fastapi_gateway_auto_generate.database import GetAllServices, StatusService, UrlService


class BuildRouteModelsUsecase:
    """The usecase is responsible for creating an instance of the 'RouteModel' model and Pydantic models.
    """

    def __init__(self) -> None:
        self.__open_api_parser: OpenApiParser = OpenApiParser()

    def execute(self, config: Config) -> list[dict[str, Any]]:
        """Launch execution of usecase
        Args:
            config (Config): The Config object with its configuration.

        Returns:
            services_result (list[dict[str, Any]]): Return a list of services, each of which stores a list of RouteModel,Pydantic models, and the service URL.
        """

        services_result: list[dict[str, Any]] = []

        get_all_info_services_model: GetAllInfoServices = GetAllInfoServices(
            page=1)

        services, err = GetAllServices(db_url=config.db_url).get_all_services(
            get_all_info_services_model=get_all_info_services_model)

        if not err is None:
            logger.warning(err)
            return services_result

        count_page: int = services["metadata"]["count_page"]

        StatusService(db_url=config.db_url).delete_all_rows()
        UrlService(db_url=config.db_url).delete_all_rows()

        if err is None:
            for _ in range(0, count_page):

                services, err = GetAllServices(db_url=config.db_url).get_all_services(
                    get_all_info_services_model=get_all_info_services_model)

                for service in services["services"]:
                    routes_model = []
                    service_result = {}

                    url = f"{service['domain']}:{service['port']}"

                    logger.debug(url)

                    status_code = self.__open_api_parser.parse_from_service(
                        url=url)

                    logger.debug(status_code)

                    StatusService(db_url=config.db_url).set_status_service(
                        id_service=service["id"],
                        status_code=status_code
                    )

                    if status_code == -1:
                        logger.warning(f"Failed to establish connection with the \"{service['name']}\" service.")
                        continue

                    ## TODO: -2

                    if status_code != 200:
                        logger.warning(f"Code error with the \"{service['name']}\" service.")
                        continue

                    for path in self.__open_api_parser.get_paths():

                        if self.__open_api_parser.check_api_gateway_tags(path=path, tag_key=APITags.AUTO_GENERATE):

                            UrlService(db_url=config.db_url).set_url_service(
                                id_service=service["id"],
                                url=path
                            )

                            path_method: str = self.__open_api_parser.get_path_method(
                                path)

                            dependencies = []

                            logger.debug(self.__open_api_parser.get_paths())

                            if not (config.jwt is None) and self.__open_api_parser.check_api_gateway_tags(
                                    path=path, tag_key=APITags.ENABLE_AUTH):
                                dependencies.append(
                                    Depends(config.jwt(service["name"], path, path_method)))

                            route_model: RouteModel = RouteModel(
                                request_method=getattr(
                                    config.fast_api_app, path_method),
                                gateway_path=f"/{service['name']}{path}",
                                service_url=url,
                                service_path=path,
                                tags=[service["name"]],
                                dependencies=dependencies
                            )

                            route_model.query_params, route_model.query_required, route_model.query_is_cookie = self.__open_api_parser.get_queries_param(
                                path=path, method=path_method)

                            route_model.form_params = self.__open_api_parser.get_body_multipart_form_data(
                                path=path, method=path_method)

                            route_model.body_params = self.__open_api_parser.get_body_application_json(
                                path=path, method=path_method
                            )

                            routes_model.append(route_model)
                        else:
                            continue

                    service_result["models"], service_result["model_output"] = self.__generate_models(
                    )
                    service_result["route_models"] = routes_model
                    service_result["service_url"] = f"{service['domain']}:{service['port']}"

                    services_result.append(service_result)

                get_all_info_services_model.page += 1

        return services_result

    def __generate_models(self):
        """Pydantic model generator from openapi.json."

        Returns:
            _uuid (str): Unique identifier as the file name.
            classes (list[str]): List of class names.
        """

        shortuuid.set_alphabet(
            "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

        project_root = os.path.dirname(
            sys.modules['fastapi_gateway_auto_generate'].__file__)

        _uuid = f"model_{shortuuid.ShortUUID().random(length=10)}"

        output = Path(f'{project_root}/tmp/models/{_uuid}.py')

        generate(
            input_=json.dumps(self.__open_api_parser.get_raw_response_in_json()),
            input_file_type=InputFileType.OpenAPI,
            input_filename="example.json",
            output=output
        )

        model: str = output.read_text()
        classes: list[str] = re.findall(r"class\s([A-Za-z0-91]*)", model)

        return _uuid, classes
