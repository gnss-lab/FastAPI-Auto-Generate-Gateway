import os.path
from fastapi_gateway_auto_generate import Generator, Config
from fastapi_gateway_auto_generate.domain.usecases import InitDatabaseUsecase
from tests.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture
from tests.services.rinex_to_csv import rinex_to_csv, rinex_to_csv_with_tags


def test_init_database_usecase(openapi_json_rinex_to_csv_fixture):
    # client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=True))

    config = Config(
        fast_api_app=rinex_to_csv_with_tags.app,
        # celery_app=celery,
        db_path="./tmp/"
    )

    InitDatabaseUsecase().execute(db_url=config.db_url, db_path=config.db_path)

    if os.path.isfile(config.get_database_absolute_path()):
        os.remove(config.get_database_absolute_path())

        assert True
    else:
        assert False
