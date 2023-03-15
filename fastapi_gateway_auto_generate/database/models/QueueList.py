from ..SQLAlchemy.declarative_base import Base

from sqlalchemy import Column, INTEGER, ForeignKey, TEXT


class QueueList(Base):
    __tablename__: str = "queue_list"

    id: Column = Column(INTEGER, primary_key=True, autoincrement=True)
    service_id: Column = Column(
        INTEGER, ForeignKey("services.id", onupdate="CASCADE", ondelete="CASCADE"), unique=True)
    name: Column = Column(TEXT, nullable=False)
