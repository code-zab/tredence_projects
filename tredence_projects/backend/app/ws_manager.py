from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
from .services.room_service import RoomService
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        conns = self.active_connections.get(room_id, [])
        if websocket in conns:
            conns.remove(websocket)
        if not conns:
            self.active_connections.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict, sender: WebSocket | None = None):
        conns = self.active_connections.get(room_id, [])
        text = json.dumps(message)
        for ws in list(conns):
            try:
                if ws is not sender:
                    await ws.send_text(text)
            except Exception:
                try:
                    conns.remove(ws)
                except ValueError:
                    pass

manager = ConnectionManager()

websocket_router = APIRouter()

@websocket_router.websocket('/ws/{room_id}')
async def websocket_endpoint(websocket: WebSocket, room_id: str, room_service: RoomService = Depends(RoomService)):
    await manager.connect(room_id, websocket)
    try:
        room = room_service.get_room(room_id)
        if room:
            await websocket.send_text(json.dumps({'type': 'init', 'code': room.code, 'language': room.language}))

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get('type') == 'update':
                code = payload.get('code', '')
                room_service.update_room_code(room_id, code)
                await manager.broadcast(room_id, {'type': 'update', 'code': code}, sender=websocket)

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    except Exception:
        manager.disconnect(room_id, websocket)
