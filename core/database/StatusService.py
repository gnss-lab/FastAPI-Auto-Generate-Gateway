from loguru import logger
from ..management.models import AddService as add_service_model
from .models import StatusServices

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..Config import Config


class StatusService():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))
        self.__session = Session()

    def set_status_service(self, id_service: int, status_code: int) -> bool:

        # Добавить проверку существование сервиса [Error Code 1]

        try:
            status_service: StatusServices = StatusServices(
                id_service=id_service,
                status_code=status_code
            )

            self.__session.add(status_service)
            self.__session.commit()

            self.__session.close()
            return True
        except Exception as e:
            logger.debug(f"Ошибка: {str(e)}")
            return False

    def delete_all_rows(self):
        try:
            self.__session.query(StatusServices).delete()
            self.__session.commit()
            return True
        except Exception as e:
            logger.debug(f"Ошибка: {str(e)}")
            return False
