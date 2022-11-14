from fastapi import APIRouter, Depends
from ..models import GetAllInfoServices

get_all_info_services_router: APIRouter = APIRouter()


@get_all_info_services_router.get("/services", tags=["Service management"])
async def get_all_services(get_all_info_service: GetAllInfoServices = Depends()) -> dict[str, str]:
    return {"data": "Hello World"}
