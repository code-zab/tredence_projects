from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime, uuid

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(Text, default='')
    language = Column(String(32), default='python')
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
