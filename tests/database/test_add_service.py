import os

from fastapi_gateway_auto_generate.database import AddService
from fastapi_gateway_auto_generate.database.models import Services
from fastapi_gateway_auto_generate.management.models import AddService as AddServiceModel
from fastapi_gateway_auto_generate.domain.usecases import InitDatabaseUsecase
from tests.builders.FakeServices import FakeServices
from tests.fixtures.get_db_session import get_db_session


def test_add_service(get_db_session):
    db_url: str = f"sqlite:///{os.path.abspath('/tmp/testdb.db')}"

    InitDatabaseUsecase().execute(db_url=db_url)

    data = next(get_db_session(db_url=db_url))

    add_service = AddService(db_url=db_url)

    count_services = 10

    for i in range(count_services):

        fake_service = FakeServices() \
            .with_domain() \
            .with_name() \
            .with_port() \
            .build()

        add_service_model = AddServiceModel(
            domain=fake_service["domain"],
            name_service=fake_service["name"],
            port=fake_service["port"]
        )


        add_service.add_service(add_service_model=add_service_model)

    assert count_services == data.query(Services).count()

    # print(FakeServices().with_domain().with_port().with_name().build().domain)
    # print(FakeServices().with_domain().with_port().with_name().build().port)
    # print(FakeServices().with_domain().with_port().with_name().build().name)
