from pydantic import BaseModel, IPvAnyAddress


class AddService(BaseModel):
    ip: IPvAnyAddress
    port: int
    name_service: str
