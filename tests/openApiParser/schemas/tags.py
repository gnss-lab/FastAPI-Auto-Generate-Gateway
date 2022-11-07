from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str
    description: str
    x_auto_generate_in_api_gateway: bool = Field(
        alias='x-auto-generate-in-api-gateway')
