from typing import Dict

from fastapi_gateway_auto_generate.database import SetMarkDeleteService as set_mark_delete_service_database
from fastapi import APIRouter, Depends, HTTPException
from ..models import DeleteService
from ...Config import Config
from ...utils import success_code


class DeleteServiceRoute:
    """Router for deleting a service
        Args:
            config (Config): The Config object with its configuration.

        Returns:
            result (bool): True if the service was successfully marked as deleted, False in case of an error.
    """

    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()
        self.__dependencies = []

        if not self.__config.jwt is None:
            self.__dependencies.append(Depends(self.__config.jwt(self.__config.service_name, "/service", "delete")))

        @self.route.delete("/service", tags=["Service management"],
                           dependencies=self.__dependencies)
        async def delete_service(delete_service: DeleteService = Depends()) -> dict[str, dict[str, str | int]]:
            result, err = set_mark_delete_service_database(db_url=self.__config.db_url).set_mark_delete_service(
                delete_service_model=delete_service)

            if err:
                raise HTTPException(status_code=409, detail=err)

            return success_code(msg="The service has been successfully marked as deleted")
