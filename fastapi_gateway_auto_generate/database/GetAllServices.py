import math
from typing import Any
from loguru import logger

from .Errors import Errors
from .models import Services
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..management.models import GetAllInfoServices as get_all_info_services_model


class GetAllServices():

    def __init__(self, db_url: str) -> None:
        Session: sessionmaker = sessionmaker(bind=create_engine(db_url))
        self.__session = Session()

    def get_all_services(self, get_all_info_services_model: get_all_info_services_model) -> tuple[None, dict[str, int | str]] | tuple[dict[str, list[Any]], None]:

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

            return result, None
        except Exception as e:
            return None, Errors.any_error(str(e))
