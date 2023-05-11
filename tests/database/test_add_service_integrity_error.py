import os
from unittest.mock import MagicMock

from sqlalchemy.exc import IntegrityError

from fastapi_gateway_auto_generate.database.Errors import Errors
from fastapi_gateway_auto_generate.database.AddService import AddService
from fastapi_gateway_auto_generate.management.models import AddService as AddServiceModel
from fastapi_gateway_auto_generate.domain.usecases import InitDatabaseUsecase
from tests.builders.FakeServices import FakeServices

def test_add_service_integrity_error():
    db_url: str = f"sqlite:///{os.path.abspath('/tmp/testdb.db')}"

    add_service = AddService(db_url)

    service_model = AddServiceModel(
        domain="http://example.com",
        port=8080,
        name_service="test_service"
    )

    with MagicMock() as mock_session:
        mock_session.add.side_effect = IntegrityError("", "", "")
        add_service._AddService__session_maker.return_value = mock_session
        add_service._AddService__session = add_service._AddService__session_maker.return_value
        result = add_service.add_service(service_model)

        assert result == (None, Errors.service_exists(name="test_service"))