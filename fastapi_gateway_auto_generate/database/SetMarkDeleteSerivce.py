from loguru import logger
from ..management.models import DeleteService as delete_service_model
from .models import Services

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..Config import Config


class SetMarkDeleteService():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))
        self.__session = Session()

    def set_mark_delete_service(self, delete_service_model: delete_service_model) -> bool:

        # Добавить проверку существование сервиса [Error Code 1]

        try:
            # service: Services = Services(
            #     domain=str(add_service_model.domain),
            #     port=add_service_model.port,
            #     name=add_service_model.name_service
            # )

            service = self.__session.query(Services).filter_by(id=delete_service_model.id_service).first()
            service.delete = True
            # print(delete_service_model.id_service)
            # self.__session.delete(service)
            self.__session.commit()

            self.__session.close()
            return True
        except Exception as e:
            logger.debug(f"Ошибка: {str(e)}")
            return False
