from fastapi_gateway_auto_generate.database import SetMarkDeleteService as set_mark_delete_service_database
from fastapi import APIRouter, Depends
from ..models import DeleteService
from ...Config import Config


class DeleteServiceRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()

        @self.route.delete("/service", tags=["Service management"])
        async def delete_service(delete_service: DeleteService = Depends()) -> dict[str, str]:
            result = set_mark_delete_service_database(db_url=self.__config.db_url).set_mark_delete_service(
                delete_service_model=delete_service)
            return result
