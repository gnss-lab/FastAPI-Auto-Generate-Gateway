from ast import List
from typing import Any
from core.OpenApiParser import OpenApiParser
from tests.openApiParser.schemas.tags import Tag
from runtime_type_checker import check_type


def get_annot(var: str) -> str:
    if var in globals():
        return globals()["__annotations__"].get(var, "Un-annotated Variable")
    else:
        return "Undefined variable"


class TestOpenApiParser:

    def test_get_tags(self, open_api_parse_file: OpenApiParser) -> None:
        tags: dict[Any, Any] = open_api_parse_file.get_tags()

        for tag in tags.values():
            Tag(**tag)

    def test_get_paths(self, open_api_parse_file: OpenApiParser) -> None:
        check_type(open_api_parse_file.get_paths(), list[str])

    def test_check_auto_generate_in_api_gateway_1(self, open_api_parse_file: OpenApiParser) -> None:
        paths: list[str] = open_api_parse_file.get_paths()[1:2]

        assert paths[0] == "/mosgim/generate-map"

        check: bool = False

        for path in paths:
            check = open_api_parse_file.check_auto_generate_in_api_gateway(
                path)

        assert check == True

    def test_check_auto_generate_in_api_gateway_2(self, open_api_parse_file: OpenApiParser) -> None:
        paths: list[str] = open_api_parse_file.get_paths()[0:1]

        assert paths[0] == "/mosgim/ping"

        check: bool = False

        for path in paths:
            check = open_api_parse_file.check_auto_generate_in_api_gateway(
                path)

        assert check == False

    def test_get_body_multipart_form_data(self, open_api_parse_file: OpenApiParser) -> None:
        paths: list[str] = open_api_parse_file.get_paths()

        # for path in paths:
        #     method = open_api_parse_file.get_body_multipart_form_data(path=)
