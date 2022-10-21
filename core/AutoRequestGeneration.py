from .RouteModel import RouteModel
from typing import List
import validators
import requests
import json


class AutoRequestGeneration:
    def __init__(self, services_url: list):

        self.__routes_model: List[RouteModel] = []
        self.__services_url: list = services_url

        self.__response_json: dict = {}
        self.__method: str = ""
        self.__auto_generate_in_api_gateway: bool = False

    def build_routes(self):
        for service_url in self.__services_url:

            route_model = RouteModel()

            if validators.url(service_url):
                pass

            self.__response_json = json.loads(
                self.__get_from_openAPI_service(service_url))

            print(route_model)

    def __get_from_openAPI_service(self, url):
        try:
            response = requests.get(
                url=f"{url}/openapi.json",
            )

            return response.content
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def __get_paths(self, response_json):
        return response_json["paths"].keys()

    def __get_method(self, response_json, path):
        return [*self.__response_json["paths"][path].keys()][0]

    def __get_tags(self, response_json):
        pass
