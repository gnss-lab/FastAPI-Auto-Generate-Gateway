from loguru import logger
from ..management.models import AddService as add_service_model
from .models import Services

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..Config import Config


class AddService():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))
        self.__session = Session()

    def add_service(self, add_service_model: add_service_model) -> bool:

        # Добавить проверку существование сервиса [Error Code 1]

        try:
            service: Services = Services(
                domain=str(add_service_model.domain),
                port=add_service_model.port,
                name=add_service_model.name_service
            )

            self.__session.add(service)
            self.__session.commit()

            self.__session.close()
            return True
        except Exception as e:
            logger.debug(f"Ошибка: {str(e)}")
            return False
