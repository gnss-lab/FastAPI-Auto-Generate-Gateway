from fastapi import APIRouter, Depends
from pydantic import BaseModel

delete_service_router: APIRouter = APIRouter()


class DeleteService(BaseModel):
    id_service: int


@delete_service_router.delete("/delete-service", tags=["Service management"])
async def delete_service(delete_service: DeleteService = Depends()) -> dict[str, str]:
    return {"data": "Hello World"}
