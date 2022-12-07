import pytest
from fastapi_gateway_auto_generate.utils.OpenApiParser import OpenApiParser


@pytest.fixture
def open_api_parse_file() -> OpenApiParser:
    open_api_parse: OpenApiParser = OpenApiParser()
    open_api_parse.parse_from_file("./tests/data/swagger.json")

    return open_api_parse
