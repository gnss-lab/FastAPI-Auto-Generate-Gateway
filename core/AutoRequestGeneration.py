import json
import string
import fastapi
import requests
import validators
from loguru import logger
from pprint import pprint
from fastapi import FastAPI
from requests import Response
from .RouteModel import RouteModel
from fastapi_gateway import route
from typing import List, NoReturn, Union, Tuple


class AutoRequestGeneration:
    def __init__(self, fast_api_app: FastAPI, services_url: list) -> NoReturn:

        self.__fast_api_app: FastAPI = fast_api_app

        self.__routes_model: List[RouteModel] = []
        self.__services_url: list = services_url

        self.__response_json: dict = {}
        self.__tags_open_api: dict = {}
        # self.__method: str = ""
        # self.__auto_generate_in_api_gateway: bool = False

    def build_routes(self) -> NoReturn:
        for service_url in self.__services_url:

            if validators.url(service_url):
                pass

            self.__response_json = json.loads(
                self.__get_from_openAPI_service(url=service_url))

            self.__tags_open_api = self.__get_tags()

            for path in self.__get_paths():

                tags_path = self.__response_json["paths"][path][self.__get_path_method(
                    path)].get("tags")

                if self.__check_auto_generate_in_api_gateway(tags_path):

                    path_method = self.__get_path_method(path)

                    route_model: RouteModel = RouteModel(
                        request_method=getattr(
                            self.__fast_api_app, path_method),
                        gateway_path=path,
                        service_url=service_url,
                        service_path=path
                    )

                    route_model.query_params, route_model.query_required = self.__get_queries_param(
                        path=path, method=path_method)

                    route_model.form_params = self.__get_body_multipart_form_data(
                        path=path, method=path_method)

                    self.__routes_model.append(route_model)
                else:
                    continue

            pprint(self.__routes_model)
        # # self.__init_functions()

    def __get_from_openAPI_service(self, url: str) -> bytes:
        """Get the microservice REST API specification

        Parameters
        ----------
        url
            Microservice URL

        Returns
        -------
        bytes
            Open API json
        """
        try:
            response: Response = requests.get(
                url=f"{url}/openapi.json",
            )

            return response.content
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def __get_paths(self) -> list:
        """Get all paths from microservice

        Returns
        -------
        list
           List of all paths
        """
        return self.__response_json["paths"].keys()

    def __get_path_method(self, path: str) -> str:
        """Get the path method

        Returns
        -------
        str
           Path method
        """
        return [*self.__response_json["paths"][path].keys()][0]

    def __get_tags(self) -> dict:
        return {fruit["name"]: fruit for fruit in self.__response_json["tags"]}

    def __get_body_multipart_form_data(self, path: str, method: str) -> Union[list, None]:
        body = self.__response_json["paths"][path][method].get("requestBody")

        if body is None:
            return None

        if body["content"].get("multipart/form-data") is None:
            logger.warning("The body is not a multipart/form-data")
            return None

        scheme_ref = body["content"].get(
            "multipart/form-data")["schema"]["$ref"]

        scheme = self.__get_body_scheme(ref=scheme_ref)

        return list(scheme["properties"].keys())

    def __get_body_scheme(self, ref: str) -> dict:
        # TODO #1: Обработать ошибку если что-то пойдет нитак
        ref_split = ref.split("/")[1:]

        path = self.__response_json[ref_split[0]]

        for i in ref_split[1:]:
            path = path[i]

        return path

    def __get_queries_param(self, path: str, method: str) -> Tuple[Union[list, None], Union[list, None]]:

        queries = self.__response_json["paths"][path][method].get("parameters")

        if queries is None:
            return None, None

        names = []
        requireds = []

        for query in queries:
            names.append(query["name"])
            requireds.append(query["required"])

        return names, requireds

    def __check_auto_generate_in_api_gateway(self, tags_path: list) -> bool:

        if not tags_path:
            return False
        else:
            for tag in tags_path:
                if not self.__tags_open_api.get(tag):
                    logger.warning(f"There is no such tag: {tag}")
                    continue

                if not self.__tags_open_api.get(tag).get("auto_generate_in_api_gateway"):
                    return False
                else:
                    # TODO #2: Добавить проверку на тип bool

                    return self.__tags_open_api.get(tag).get("auto_generate_in_api_gateway")

    def __save_open_api_database(self):
        pass