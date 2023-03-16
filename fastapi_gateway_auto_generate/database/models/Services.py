from dataclasses import dataclass
from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import relationship, backref
from typing import Any
from loguru import logger


class Services(Base):
    __tablename__: str = "services"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    domain: Column = Column(TEXT, nullable=False)
    port: Column = Column(INTEGER, nullable=False)
    name: Column = Column(TEXT, nullable=False, unique=True)
    delete: Column = Column(BOOLEAN, nullable=False, default=False)

    urls: Any = relationship(
        "UrlServices", cascade='all,delete', backref=backref("services"))

    status: Any = relationship(
        "StatusServices", cascade='all,delete', backref=backref("services"))

    def obj_to_dict(self) -> dict[str, Column]:

        urls: list[str] = []
        status_code: int = 0

        for url in self.urls:
            urls.append(url.url)

        # for status in self.status:
        #     status_code
        for service in self.status:
            status_code = service.status_code

        return {
            "id": self.id,
            "domain": self.domain,
            "port": self.port,
            "name": self.name,
            "urls": urls,
            "status-code": status_code,
            "delete": self.delete
        }
