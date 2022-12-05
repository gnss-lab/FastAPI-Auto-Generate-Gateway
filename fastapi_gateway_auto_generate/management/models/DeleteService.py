from pydantic import BaseModel


class DeleteService(BaseModel):
    id_service: int
