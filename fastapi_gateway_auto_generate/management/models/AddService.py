from pydantic import BaseModel, validator, ValidationError
import validators
from typing import Any
from loguru import logger


class AddService(BaseModel):
    domain: str
    name_service: str
    port: int = 80
    allow_large_files: bool = False

    @validator('domain')
    def domain_validation(cls, v):
        assert True == validators.url(v), "Invalid domain"
        return v
