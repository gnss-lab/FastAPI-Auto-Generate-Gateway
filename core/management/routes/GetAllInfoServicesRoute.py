from fastapi import APIRouter, Depends, HTTPException
from ..models import GetAllInfoServices
from core.database import GetAllServices
from ...Config import Config

get_all_info_services_router: APIRouter = APIRouter()


class GetAllInfoServicesRoute:

    def __init__(self, config: Config) -> None:

        self.__config: Config = config
        self.route: APIRouter = APIRouter()

        @self.route.get("/services", tags=["Service management"])
        async def get_all_services(get_all_info_service: GetAllInfoServices = Depends()) -> dict[str, str]:

            result, err = GetAllServices(db_url=self.__config.db_url).get_all_services(
                get_all_info_services_model=get_all_info_service)

            if not err is None:
                raise HTTPException(status_code=400, detail={
                                    "code": err["code"], "err_msg": err["msg"]})

            return result
