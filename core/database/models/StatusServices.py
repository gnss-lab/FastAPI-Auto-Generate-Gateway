from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, ForeignKey


class StatusServices(Base):
    __tablename__: str = "status_services"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    id_service: Column = Column(
        INTEGER, ForeignKey("services.id", onupdate="CASCADE", ondelete="CASCADE"), unique=True)
    status_code: Column = Column(INTEGER, nullable=False)
