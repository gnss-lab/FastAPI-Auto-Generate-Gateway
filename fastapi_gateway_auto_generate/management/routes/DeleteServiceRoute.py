from fastapi import APIRouter, Depends
from ..models import DeleteService
from ...Config import Config


class DeleteServiceRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()

        @self.route.delete("/service", tags=["Service management"])
        async def delete_service(delete_service: DeleteService = Depends()) -> dict[str, str]:
            return {"data": "Hello World"}
