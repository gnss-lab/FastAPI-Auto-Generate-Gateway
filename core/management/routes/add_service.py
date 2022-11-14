from fastapi import APIRouter, Depends
from pydantic import BaseModel, IPvAnyAddress

add_service_router: APIRouter = APIRouter()


class AddService(BaseModel):
    ip: IPvAnyAddress
    port: int
    name_service: str


@add_service_router.post("/add_service", tags=["Service management"])
async def add_service(add_service: AddService = Depends()) -> dict[str, str]:
    return {"data": "Hello World"}
