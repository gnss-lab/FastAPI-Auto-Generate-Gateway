
# DATA_TYPES = {
#     "integer": "int",
#     "number": "float",
#     "string": "str",
#     "boolean": "bool",

# }

import json
import requests
from requests import Response
from typing import Any
from datamodel_code_generator import InputFileType, generate
from io import StringIO
from pathlib import Path
from pprint import pprint
from pydantic import BaseModel, Field

TAG = "x-auto-generate-in-api-gateway"


class OpenApiParser:
    def __init__(self):
        self.__data_types: dict[str, str] = {
            "integer": "int",
            "number": "float",
            "string": "str",
            "boolean": "bool",
        }

        self.__response_json: dict[Any, Any] = {}
        self.__tags_open_api: dict[Any, Any] = {}

    def parse_from_service(self, url: str) -> None:
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

            self.__response_json = json.loads(response.content)
            self.__tags_open_api = self.get_tags()

        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("HTTP Request failed")

    def parse_from_file(self, file_path: str) -> None:
        with open(file_path) as json_file:
            self.__response_json = json.load(json_file)
            self.__tags_open_api = self.get_tags()

    def get_tags(self) -> dict[Any, Any]:

        if self.__response_json.get("tags") is None:
            return {}
        else:
            return {fruit["name"]: fruit for fruit in self.__response_json.get("tags")}

    def get_paths(self) -> list[str]:
        """Get all paths from microservice

        Returns
        -------
        list
           List of all paths
        """

        return list(self.__response_json["paths"].keys())

    def get_path_method(self, path: str) -> str:
        """Get the path method

        Returns
        -------
        str
           Path method
        """
        return [*self.__response_json["paths"][path].keys()][0]

    def get_path_tags(self, path: str) -> list[str]:
        return self.__response_json["paths"][path][self.get_path_method(path)].get("tags")

    def get_body_multipart_form_data(self, path: str, method: str) -> list[str] | None:
        body: dict[Any, Any] = self.__response_json["paths"][path][method].get(
            "requestBody")

        if body is None:
            return None

        if body["content"].get("multipart/form-data") is None:
            # logger.warning("The body is not a multipart/form-data")
            return None

        scheme_ref: str = body["content"].get(
            "multipart/form-data")["schema"]["$ref"]

        scheme: dict[Any, Any] = self.get_body_scheme(ref=scheme_ref)

        return list(scheme["properties"].keys())

    def get_body_scheme(self, ref: str) -> dict[Any, Any]:
        # TODO #1: Обработать ошибку если что-то пойдет нитак
        ref_split: list[str] = ref.split("/")[1:]

        path: dict[Any, Any] = self.__response_json[ref_split[0]]

        for i in ref_split[1:]:
            path = path[i]

        return path

    def get_queries_param(self, path: str, method: str) -> tuple[None, None] | tuple[list[str], list[bool]]:

        queries: list[dict[Any, Any]] = self.__response_json["paths"][path][method].get(
            "parameters")

        if queries is None:
            return None, None

        names: list[str] = []
        requireds: list[bool] = []

        for query in queries:
            names.append(query["name"])
            requireds.append(query["required"])

        return names, requireds

    def check_auto_generate_in_api_gateway(self, path: str) -> bool:

        tags_path: list[str] = self.get_path_tags(path=path)

        if tags_path:
            for tag in tags_path:
                if not self.__tags_open_api.get(tag):
                    # logger.warning(f"There is no such tag: {tag}")
                    continue

                if not self.__tags_open_api.get(tag).get(TAG):
                    return False
                else:
                    # TODO #2: Добавить проверку на тип bool

                    return self.__tags_open_api.get(tag).get(TAG)

        return False

    def get_raw_response_in_json(self) -> dict[Any, Any]:
        return self.__response_json

    def get_raw_resoponse_in_string(self) -> str:
        return json.dumps(self.__response_json)
