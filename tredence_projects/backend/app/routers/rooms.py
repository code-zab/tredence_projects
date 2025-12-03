from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, db
import uuid
from ..schemas import CreateRoomResp

router = APIRouter()

@router.post('/', response_model=CreateRoomResp)
def create_room(db: Session = Depends(db.get_db)):
    r = models.Room()
    db.add(r)
    db.commit()
    db.refresh(r)
    return {'roomId': r.id}

@router.get('/{room_id}')
def get_room(room_id: str, db: Session = Depends(db.get_db)):
    try:
        rid = uuid.UUID(room_id)
    except ValueError:
        raise HTTPException(status_code=400, detail='invalid room id')
    room = db.query(models.Room).filter(models.Room.id == rid).first()
    if not room:
        raise HTTPException(status_code=404, detail='room not found')
    return {'roomId': str(room.id), 'code': room.code, 'language': room.language}
