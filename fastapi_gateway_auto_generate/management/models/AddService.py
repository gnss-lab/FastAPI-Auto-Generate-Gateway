from pydantic import BaseModel, validator, ValidationError
import validators
from typing import Any
from loguru import logger


class AddService(BaseModel):
    domain: str
    name_service: str
    port: int = 80

    @validator('domain')
    def domain_validation(cls, v):
        assert True == validators.url(v), "Invalid domain"
        return v
