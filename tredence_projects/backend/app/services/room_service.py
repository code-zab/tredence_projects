from ..db import get_db
from .. import models
from typing import Optional
from sqlalchemy.orm import Session
import uuid

class RoomService:
    def __init__(self, db: Session = None):
        self._db = next(get_db()) if db is None else db

    def get_room(self, room_id: str) -> Optional[models.Room]:
        try:
            rid = uuid.UUID(room_id)
        except Exception:
            return None
        return self._db.query(models.Room).filter(models.Room.id == rid).first()

    def update_room_code(self, room_id: str, code: str):
        room = self.get_room(room_id)
        if room:
            room.code = code
            from datetime import datetime
            room.updated_at = datetime.utcnow()
            self._db.add(room)
            self._db.commit()
            self._db.refresh(room)
            return room
        else:
            r = models.Room()
            r.code = code
            self._db.add(r)
            self._db.commit()
            self._db.refresh(r)
            return r
