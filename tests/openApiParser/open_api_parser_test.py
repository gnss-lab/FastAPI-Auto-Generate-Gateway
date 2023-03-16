import json

import pytest
from unittest.mock import Mock, patch

import requests

from fastapi_gateway_auto_generate.utils.OpenApiParser import (OpenApiParser,
                                                               TAG_AUTO_GENERATE,
                                                               TAG_ENABLE_AUTH,
                                                               TAG_LARGE_FILE)

from tests.openApiParser.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture
from tests.openApiParser.fixtures.parser_rinex_to_csv_fixture import parser_rinex_to_csv_fixture
from tests.openApiParser.microservices import rinex_to_csv

OPEN_API_PARSE_REQUEST_GET = "fastapi_gateway_auto_generate.utils.OpenApiParser.requests.get"


class TestOpenApiParser:

    @pytest.mark.parametrize("tags", [False, True])
    def test_parse_from_service(self, openapi_json_rinex_to_csv_fixture, tags):
        parser = OpenApiParser()

        client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=tags))

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = openapi.encode()

        with patch(OPEN_API_PARSE_REQUEST_GET, return_value=mock_response):
            result = parser.parse_from_service('http://example.com')

            assert result == 200

            assert parser.get_raw_response_in_json() == json.loads(openapi)

            if tags:
                tags_open_api = getattr(parser, '_OpenApiParser__tags_open_api')
                assert tags_open_api != {}

    def test_parse_from_service_exception(self):
        with patch(OPEN_API_PARSE_REQUEST_GET) as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException

            parser = OpenApiParser()
            status_code = parser.parse_from_service('http://example.com')

            assert status_code == -1
            assert parser.get_raw_response_in_json() == {}

    def test_get_paths(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        urls = [route.path for route in rinex_to_csv.app.routes]

        for path in paths:
            assert path in urls

    def test_get_path_method(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        for path in paths:
            route = rinex_to_csv.app.routes[4 + paths.index(path)]
            assert parser.get_path_method(path) == route.methods.pop().lower()

    def test_get_path_method(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        for path in paths:
            route = rinex_to_csv.app.routes[4 + paths.index(path)]
            assert parser.get_path_method(path) == route.methods.pop().lower()

    @pytest.mark.parametrize("path, expected", [
        ("/rinex_to_csv/upload_rinex", False),
        ("/rinex_to_csv/upload_nav", True),
        ("/rinex_to_csv/run", False),
        ("/rinex_to_csv/get_result", True),
    ])
    def test_auto_generate_enabled(self, parser_rinex_to_csv_fixture, path, expected):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture(tags=True))

        assert parser.auto_generate_enabled(path=path) == expected