from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, TEXT, ForeignKey


class UrlServices(Base):
    __tablename__: str = "url_services"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    id_service: Column = Column(
        INTEGER, ForeignKey("services.id", onupdate="CASCADE", ondelete="CASCADE"))
    url: Column = Column(TEXT, nullable=False, unique=True)
