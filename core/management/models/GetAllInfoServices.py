from pydantic import BaseModel


class GetAllInfoServices(BaseModel):
    page: int = 1
