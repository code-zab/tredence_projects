from pydantic import BaseModel
import uuid

class CreateRoomResp(BaseModel):
    roomId: uuid.UUID

class AutocompleteReq(BaseModel):
    code: str
    cursorPosition: int
    language: str = 'python'

class AutocompleteResp(BaseModel):
    suggestion: str
