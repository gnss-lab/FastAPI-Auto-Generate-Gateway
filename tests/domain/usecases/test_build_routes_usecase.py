import os
from pprint import pprint
from unittest.mock import Mock, patch
import json
from fastapi import openapi, FastAPI
from openapi_parser import OpenApiParser
from fastapi.testclient import TestClient

from fastapi_gateway_auto_generate import Config
from fastapi_gateway_auto_generate.domain.usecases import BuildRouteModelsUsecase, InitDatabaseUsecase, \
    BuildRoutesUsecase
from fastapi_gateway_auto_generate.management.models import AddService
from tests.services.rinex_to_csv import rinex_to_csv, rinex_to_csv_with_tags
from fastapi_gateway_auto_generate.database import AddService as add_service_database
from tests.builders.FakeServices import FakeServices
from tests.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture


def test_build_routes_usecase(openapi_json_rinex_to_csv_fixture):
    client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=True))

    usecase = BuildRoutesUsecase()

    app = FastAPI()
    client = TestClient(app)

    config = Config(
        fast_api_app=client.app,
        db_path="./tmp/",
    )

    InitDatabaseUsecase().execute(db_url=config.db_url, db_path=config.db_path)

    fake_service = FakeServices().with_domain().with_name().with_port().build()
    add_service_model = AddService(
        domain=fake_service["domain"],
        name_service=fake_service["name"],
        port=fake_service["port"]
    )
    add_service_database(db_url=config.db_url).add_service(add_service_model=add_service_model)

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = 200
        mock_parse.content = openapi.encode()
        mock_get.return_value = mock_parse

        build_route_models = BuildRouteModelsUsecase()
        services_result = build_route_models.execute(config=config)

    usecase.execute(services_result=services_result, fast_api_app=config.fast_api_app)

    response = client.get("/openapi.json")

    with patch('openapi_parser.OpenApiParser.requests.get') as mock_get:
        mock_parse = Mock()
        mock_parse.status_code = 200
        mock_parse.content = response.text
        mock_get.return_value = mock_parse

        open_api_parser = OpenApiParser()
        open_api_parser.parse_from_service("http://0.0.0.0")

        mock_parse.content = openapi.encode()

        open_api_parser_rinex_to_csv = OpenApiParser()
        open_api_parser_rinex_to_csv.parse_from_service("http://0.0.0.0")

    paths = open_api_parser.get_paths()
    paths_rinex = open_api_parser_rinex_to_csv.get_paths()


    paths_rinex_tmp = [f"/{fake_service['name']}" + item for item in paths_rinex][0:4]

    # pprint(paths)
    # pprint(paths_rinex_tmp)

    assert sorted(paths) == sorted(paths_rinex_tmp)
        # assert path == f""

    # with open("response.json", "w") as file:
    #     json.dump(response.json(), file, sort_keys=True, indent=4)

    # pprint(response.json())

    os.remove(config.get_database_absolute_path())