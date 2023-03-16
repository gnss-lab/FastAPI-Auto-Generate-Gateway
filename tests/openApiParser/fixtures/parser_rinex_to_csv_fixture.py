from unittest.mock import Mock, patch

import pytest

from fastapi_gateway_auto_generate.utils.OpenApiParser import OpenApiParser
from .openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture


@pytest.fixture(scope="function")
def parser_rinex_to_csv_fixture(openapi_json_rinex_to_csv_fixture):
    def _parser_rinex_to_csv_fixture(tags=False):
        parser = OpenApiParser()

        client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=tags))

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = openapi.encode()

        with patch('fastapi_gateway_auto_generate.utils.OpenApiParser.requests.get', return_value=mock_response):
            parser.parse_from_service('http://example.com')

            yield parser

    return _parser_rinex_to_csv_fixture
