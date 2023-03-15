import json

import pytest
from unittest.mock import Mock, patch

from fastapi_gateway_auto_generate.utils.OpenApiParser import OpenApiParser
from tests.openApiParser.fixtures.openapi_json_rinex_to_csv import openapi_json_rinex_to_csv

@pytest.fixture
def mock_response(monkeypatch, openapi_json_rinex_to_csv):
    # Заменяем requests.get на фиктивную функцию, которая возвращает заданный объект Response
    def get_mock(*args, **kwargs):
        class MockResponse:
            def __init__(self, status_code, content):
                self.status_code = status_code
                self.content = content

            def json(self):
                return json.loads(self.content)

        return MockResponse(200, openapi_json_rinex_to_csv.encode())

    monkeypatch.setattr("requests.get", get_mock)

class TestOpenApiParser:

    @pytest.mark.parametrize("tags", [False, True])
    def test_parse_from_service(self, openapi_json_rinex_to_csv, tags):
        parser = OpenApiParser()

        client, openapi = next(openapi_json_rinex_to_csv(tags=tags))

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = openapi.encode()

        with patch('fastapi_gateway_auto_generate.utils.OpenApiParser.requests.get', return_value=mock_response):
            result = parser.parse_from_service('http://example.com')

            assert result == (False, 200)

            assert parser.get_raw_response_in_json() == json.loads(openapi)

            if tags:
                tags_open_api = getattr(parser, '_OpenApiParser__tags_open_api')
                assert tags_open_api != {}



