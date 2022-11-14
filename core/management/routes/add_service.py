from fastapi import APIRouter, Depends
from ..models import AddService

add_service_router: APIRouter = APIRouter()


@add_service_router.post("/service", tags=["Service management"])
async def add_service(add_service: AddService = Depends()) -> dict[str, str]:
    return {"data": "Hello World"}
