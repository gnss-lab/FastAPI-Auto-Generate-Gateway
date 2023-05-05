import os

from fastapi_gateway_auto_generate.database import AddService
from fastapi_gateway_auto_generate.database.models import Services
from fastapi_gateway_auto_generate.management.models import AddService as AddServiceModel
from fastapi_gateway_auto_generate.domain.usecases import InitDatabaseUsecase
from tests.builders.FakeServices import FakeServices
from tests.fixtures.get_db_session import get_db_session


def test_add_service(get_db_session):
    db_name = "testdb"
    db_path = os.path.abspath('./tmp/database/')
    db_url: str = f"sqlite:///{db_path}/{db_name}.db"

    InitDatabaseUsecase().execute(db_url=db_url, db_path=db_path)

    data = next(get_db_session(db_url=db_url)).query(Services)

    add_service = AddService(db_url=db_url)

    count_services = 10

    for i in range(count_services):
        fake_service = (
            FakeServices()
            .with_domain()
            .with_name()
            .with_port()
            .build()
        )

        add_service_model = AddServiceModel(
            domain=fake_service["domain"],
            name_service=fake_service["name"],
            port=fake_service["port"]
        )

        add_service.add_service(add_service_model=add_service_model)

    assert count_services == data.count()

    if os.path.isfile(f"{db_path}/{db_name}.db"):
        os.remove(f"{db_path}/{db_name}.db")
        os.rmdir(db_path)
        assert True
    else:
        assert False
