from loguru import logger
from ..management.models import AddService as add_service_model
from .models import UrlServices

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..Config import Config


class UrlService():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))
        self.__session = Session()

    def set_url_service(self, id_service: int, url: str) -> bool:

        # Добавить проверку существование сервиса [Error Code 1]

        try:
            url_service: UrlServices = UrlServices(
                id_service=id_service,
                url=url
            )

            self.__session.add(url_service)
            self.__session.commit()

            self.__session.close()
            return True
        except Exception as e:
            logger.error(str(e))
            return False

    def delete_all_rows(self):
        try:
            self.__session.query(UrlServices).delete()
            self.__session.commit()
            return True
        except Exception as e:
            logger.error(f"Ошибка: {str(e)}")
            return False
