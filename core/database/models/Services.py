from dataclasses import dataclass
from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, TEXT


class Services(Base):
    __tablename__: str = "fast_api_auto_generate_services"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    ip: Column = Column(INTEGER, nullable=False)
    port: Column = Column(INTEGER, nullable=False)
    name: Column = Column(TEXT, nullable=False, unique=True)

    def obj_to_dict(self):  # for build json format
        return {
            "id": self.id,
            "ip": self.ip,
            "port": self.port,
            "name": self.name
        }
