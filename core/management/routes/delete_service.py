from fastapi import APIRouter, Depends
from ..models import DeleteService

delete_service_router: APIRouter = APIRouter()


@delete_service_router.delete("/service", tags=["Service management"])
async def delete_service(delete_service: DeleteService = Depends()) -> dict[str, str]:
    return {"data": "Hello World"}
