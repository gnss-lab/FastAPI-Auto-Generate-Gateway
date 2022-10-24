from .RouteModel import RouteModel
from typing import List, NoReturn
import validators
import requests
from requests import Response
import json
from fastapi import FastAPI
import fastapi
from warnings import warn
from fastapi_gateway import route


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
                    route_model: RouteModel = RouteModel(
                        request_method=getattr(
                            self.__fast_api_app, self.__get_path_method(path)),
                        gateway_path=path,
                        service_url=service_url,
                        service_path=path
                    )

                self.__routes_model.append(route_model)

            print(route_model)

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

    def __check_auto_generate_in_api_gateway(self, tags_path: list) -> bool:

        if not tags_path:
            return False
        else:
            for tag in tags_path:
                if not self.__tags_open_api.get(tag):
                    warn(f"There is no such tag: {tag}")
                    continue

                if not self.__tags_open_api.get(tag).get("auto_generate_in_api_gateway"):
                    return False
                else:
                    # TODO #1: Добавить проверку на тип bool

                    return self.__tags_open_api.get(tag).get("auto_generate_in_api_gateway")
