from fastapi import APIRouter, Depends
from pydantic import BaseModel

get_all_services_router: APIRouter = APIRouter()


class GetAllServices(BaseModel):
    id_service: int


@get_all_services_router.get("/get-all-services", tags=["Service management"])
async def get_all_services(page: int) -> dict[str, str]:
    return {"data": "Hello World"}
