from loguru import logger
from ..management.models import GetAllInfoServices as get_all_info_services_model
from .models import Services

from sqlalchemy.orm import sessionmaker

from typing import Any
from pprint import pprint
import json
import math
from sqlalchemy import create_engine


class GetAllServices():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(bind=create_engine(db_url))
        self.__session = Session()

    def get_all_services_json(self, get_all_info_services_model: get_all_info_services_model) -> dict[Any, Any]:

        # Добавить проверку существование сервиса [Error Code 1]
        try:
            start = 0 + (get_all_info_services_model.page - 1) * 10

            rows_count: int = self.__session.query(Services).count()
            count_page = math.ceil(rows_count / 10)

            if count_page < 0 or count_page < get_all_info_services_model.page:
                return {"data": " Такой страницы не существует"}

            services = self.__session.query(
                Services).limit(10).offset(start).all()

            if not services:
                return {"data": "Ничего не найдено"}

            result = {"services": [item.obj_to_dict() for item in services]}

            result["metadata"] = [{
                "page": get_all_info_services_model.page,
                "count_page": math.ceil(rows_count / 10)}]

            # pprint(result)
            # logger.debug(services)
            # service: Services = Services(
            #     ip=str(add_service_model.ip),
            #     port=add_service_model.port,
            #     name=add_service_model.name_service
            # )

            # self.__session.add(service)
            # self.__session.commit()

            # self.__session.close()
            return result
        except Exception as e:
            logger.debug(f"Ошибка: {str(e)}")
            return {}
