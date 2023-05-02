from typing import Tuple, Optional, Union

from loguru import logger

from .Errors import Errors
from ..management.models import AddService as add_service_model
from .models import Services

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

ServiceResult = Tuple[Optional[bool], Optional[dict[str, Union[int, str]]]]


class AddService():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))
        self.__session = Session()

    def add_service(self, add_service_model: add_service_model) -> ServiceResult:

        domain = str(add_service_model.domain)
        port = add_service_model.port
        name = add_service_model.name_service

        try:
            service: Services = Services(
                domain=domain,
                port=port,
                name=name
            )

            self.__session.add(service)
            self.__session.commit()

            self.__session.close()

            return True, None
        except IntegrityError as i:
            return None, Errors.service_exists(name=name)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return None, Errors.any_error(str(e))
