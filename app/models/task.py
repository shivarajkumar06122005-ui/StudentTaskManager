
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from app.database.connection import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    completed = Column(Boolean, default=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
