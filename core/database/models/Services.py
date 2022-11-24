from dataclasses import dataclass
from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, TEXT


class Services(Base):
    __tablename__: str = "services"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    domain: Column = Column(TEXT, nullable=False)
    port: Column = Column(INTEGER, nullable=False)
    name: Column = Column(TEXT, nullable=False, unique=True)

    def obj_to_dict(self) -> dict[str, Column]:
        return {
            "id": self.id,
            "domain": self.domain,
            "port": self.port,
            "name": self.name
        }
