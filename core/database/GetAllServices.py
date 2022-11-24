from loguru import logger
from ..management.models import GetAllInfoServices as get_all_info_services_model
from .models import Services

from sqlalchemy.orm import sessionmaker

from typing import Any
from pprint import pprint
import json
import math
from sqlalchemy import create_engine
from .Errors import Errors


class GetAllServices():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(bind=create_engine(db_url))
        self.__session = Session()

    def get_all_services(self, get_all_info_services_model: get_all_info_services_model) -> tuple[None, dict[str, int | str]] | tuple[dict[str, list[Any]], None]:

        # Добавить проверку существование сервиса [Error Code 1]
        try:
            rows_count: int = self.__session.query(Services).count()

            if rows_count == 0:
                return None, Errors.no_services_found()

            start = 0 + (get_all_info_services_model.page - 1) * 10

            count_page = math.ceil(rows_count / 10)

            if count_page < 0 or count_page < get_all_info_services_model.page:
                return None, Errors.page_not_found()

            services = self.__session.query(
                Services).limit(10).offset(start).all()

            result = {"services": [item.obj_to_dict() for item in services]}

            result["metadata"] = {
                "page": get_all_info_services_model.page,
                "count_page": math.ceil(rows_count / 10)}

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
            return result, None
        except Exception as e:
            return None, Errors.any_error(str(e))
