from fastapi import APIRouter
refresh_services_router: APIRouter = APIRouter()


@refresh_services_router.patch("/services", tags=["Service management"])
async def refresh_services() -> dict[str, str]:
    return {"data": "Hello World"}
