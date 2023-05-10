import os
from pprint import pprint
from unittest.mock import Mock, patch

from openapi_parser import OpenApiParser

from fastapi_gateway_auto_generate import Config
from fastapi_gateway_auto_generate.domain.usecases import BuildRouteModelsUsecase, InitDatabaseUsecase
from fastapi_gateway_auto_generate.management.models import AddService
from tests.services.rinex_to_csv import rinex_to_csv, rinex_to_csv_with_tags
from fastapi_gateway_auto_generate.database import AddService as add_service_database
from tests.builders.FakeServices import FakeServices
from tests.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture


def JWT(service_name, path, path_method):
    pass


def test_build_route_models_usecase(openapi_json_rinex_to_csv_fixture):
    client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=True))

    config = Config(
        fast_api_app=rinex_to_csv_with_tags.app,
        db_path="./tmp/",
        jwt=JWT
    )

    InitDatabaseUsecase().execute(db_url=config.db_url, db_path=config.db_path)

    fake_service = FakeServices().with_domain().with_name().with_port().build()
    add_service_model = AddService(
        domain=fake_service["domain"],
        name_service=fake_service["name"],
        port=fake_service["port"]
    )
    add_service_database(db_url=config.db_url).add_service(add_service_model=add_service_model)

    fake_service_fail = FakeServices().with_domain().with_name().with_port().build()
    add_service_model_fail = AddService(
        domain=fake_service_fail["domain"],
        name_service=fake_service_fail["name"],
        port=fake_service_fail["port"]
    )
    add_service_database(db_url=config.db_url).add_service(add_service_model=add_service_model_fail)

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = 200
        mock_parse.content = openapi.encode()
        mock_get.return_value = mock_parse

        usecase = BuildRouteModelsUsecase()
        result = usecase.execute(config=config)

        pprint(result)

        models_name = result[0]["models"]
        route_models = result[0]["route_models"]
        model_output = result[0]["model_output"]

        # TODO: Дополнить тестами

        for i in range(len(route_models)):
            assert route_models[i].service_url == f"{fake_service['domain']}:{fake_service['port']}"
            assert route_models[i].tags[0] == fake_service['name']

        assert all(model_name in model_output for model_name in [
            'BodyUploadNavRinexToCsvUploadNavPost',
            'BodyUploadRinexRinexToCsvUploadRinexPost',
            'ConversionParams',
            'ValidationError',
            'HTTPValidationError']
                   )

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = -1
        mock_parse.content = openapi.encode()
        mock_get.return_value = mock_parse

        usecase = BuildRouteModelsUsecase()
        result = usecase.execute(config=config)
        assert result == []

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = 505
        mock_parse.content = openapi.encode()
        mock_get.return_value = mock_parse

        usecase = BuildRouteModelsUsecase()
        result = usecase.execute(config=config)
        assert result == []

    os.remove(config.get_database_absolute_path())

    usecase = BuildRouteModelsUsecase()
    result = usecase.execute(config=config)

    assert result == []
