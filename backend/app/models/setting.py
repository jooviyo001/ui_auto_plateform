from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base

class Setting(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(20), default='string')  # string, int, bool, json
    group: Mapped[str] = mapped_column(String(32), default='general')  # general, notify, integration
    description: Mapped[str] = mapped_column(String(128))