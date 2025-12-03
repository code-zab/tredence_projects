import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import rooms, autocomplete
from .ws_manager import websocket_router

app = FastAPI(title='realtime-pair-backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(rooms.router, prefix='/rooms', tags=['rooms'])
app.include_router(autocomplete.router, prefix='', tags=['autocomplete'])
app.include_router(websocket_router)

@app.get('/')
async def root():
    return {'status':'ok'}
