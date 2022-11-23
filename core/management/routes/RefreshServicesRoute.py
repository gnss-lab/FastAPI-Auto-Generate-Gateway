from fastapi import APIRouter
from ...Config import Config


class RefreshServicesRoute:
    def __init__(self, config: Config) -> None:
        self.__config: Config = config
        self.route: APIRouter = APIRouter()

        @self.route.patch("/services", tags=["Service management"])
        async def refresh_services() -> dict[str, str]:
            return {"data": "Hello World"}
