import os
from unittest.mock import Mock, patch

from openapi_parser import OpenApiParser

from fastapi_gateway_auto_generate import Config
from fastapi_gateway_auto_generate.domain.usecases import BuildRouteModelsUsecase, InitDatabaseUsecase
from fastapi_gateway_auto_generate.management.models import AddService
from tests.services.rinex_to_csv import rinex_to_csv, rinex_to_csv_with_tags
from fastapi_gateway_auto_generate.database import AddService as add_service_database
from tests.builders.FakeServices import FakeServices
from tests.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture
def test_build_route_models_usecase(openapi_json_rinex_to_csv_fixture):
    client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=True))

    config = Config(
        fast_api_app=rinex_to_csv_with_tags.app,
        # celery_app=celery,
        db_path="./tmp/"
    )

    InitDatabaseUsecase().execute(db_url=config.db_url, db_path=config.db_path)

    fake_service = (
        FakeServices()
        .with_domain()
        .with_name()
        .with_port()
        .build()
    )

    add_service_model = AddService(
        domain=fake_service["domain"],
        name_service=fake_service["name"],
        port=fake_service["port"]
    )

    add_service_database(db_url=config.db_url).add_service(
        add_service_model=add_service_model)

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = 200
        mock_parse.content = openapi.encode()

        mock_get.return_value = mock_parse
        # mock_parse.parse_from_service.response.status_code = 200
        # mock_parse.parse_from_service.response.content = openapi.encode()

        usecase = BuildRouteModelsUsecase()
        # usecase._BuildRouteModelsUsecase__open_api_parser = mock_parse
        usecase.execute(config=config)

    if os.path.isfile(config.get_database_absolute_path()):
        os.remove(config.get_database_absolute_path())

        assert True
    else:
        assert False
