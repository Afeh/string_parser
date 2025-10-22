from sqlalchemy import Column, String, JSON, DateTime
from .database import Base
from datetime import datetime, timezone

class StringRecord(Base):
    __tablename__ = "strings"

    id = Column(String, primary_key=True)
    value = Column(String, unique=True, nullable=False)
    properties = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
