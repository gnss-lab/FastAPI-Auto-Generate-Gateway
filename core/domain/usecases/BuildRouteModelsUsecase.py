# from loguru import logger
from ...utils.OpenApiParser import OpenApiParser
from ..models import RouteModel
from fastapi import FastAPI
from core.database import GetAllServices, StatusService, UrlService
from ...Config import Config
from loguru import logger
from core.management.models import GetAllInfoServices
from datamodel_code_generator import InputFileType, generate
import re
from pathlib import Path
import uuid
from typing import Any
from pprint import pprint
import os
import random
import string


class BuildRouteModelsUsecase:
    def __init__(self) -> None:
        self.__open_api_parser: OpenApiParser = OpenApiParser()

    def execute(self, config: Config) -> list[dict[str, Any]]:

        routes_model: list[RouteModel] = []
        # models: dict[str, str] | None = {}
        services_result: list[dict[str, Any]] = []

        get_all_info_services_model: GetAllInfoServices = GetAllInfoServices(
            page=1)

        services, err = GetAllServices(db_url=config.db_url).get_all_services(
            get_all_info_services_model=get_all_info_services_model)

        if not err is None:
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

                            UrlService(db_url=config.db_url).set_url_service(
                                id_service=service["id"],
                                url=path
                            )

                            path_method: str = self.__open_api_parser.get_path_method(
                                path)

                            route_model: RouteModel = RouteModel(
                                request_method=getattr(
                                    config.fast_api_app, path_method),
                                gateway_path=f"/{service['name']}{path}",
                                service_url=url,
                                service_path=path,
                                tags=[service["name"]]
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

        pprint(services_result)

        return services_result

    def __generate_models(self):

        letters = string.ascii_lowercase
        _uuid = ''.join(random.choice(letters) for _ in range(8))

        temporary_directory = Path(
            Path.home() / "Documents/xitowzys/ISZF/fastapi-gateway-auto-generate")

        output = Path(temporary_directory /
                      f'tmp/models/{_uuid}.py')

        dir = Path(temporary_directory /
                   f'tmp/models/')

        # for f in os.listdir(dir):
        #     os.remove(os.path.join(dir, f))

        generate(
            input_=self.__open_api_parser.get_raw_resoponse_in_string(),
            input_file_type=InputFileType.OpenAPI,
            input_filename="example.json",
            output=output
        )

        # vars = {}
        model: str = output.read_text()
        classes: list[str] = re.findall(r"class\s([A-Za-z0-91]*)", model)

        # print(classes)
        # exit()
        # # exec(model, vars)
        # output.unlink()

        return _uuid, classes
