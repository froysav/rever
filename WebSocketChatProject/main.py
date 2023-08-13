import base64
from typing import List, Dict
from starlette.responses import HTMLResponse
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from cryptography.fernet import Fernet
import base64

from starlette.websockets import WebSocketDisconnect

app = FastAPI()

app.mount("/static", StaticFiles(directory="/app/Frontend/static"), name="static")

# @app.get('/chat', response_class=HTMLResponse)
# async def chat():
#     with open('Frontend/static/index.html') as f:
#         return f.read()


class WebSocketManager:
    def __init__(self):
        self.active_connections = []
        # self.active_connections: List[WebSocket] = []
        # self.encryption_key = Fernet.generate_key()
        # self.cipher_suite = Fernet(self.encryption_key)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # encrypted_message = self.cipher_suite.encrypt(message.encode())
        for connection in self.active_connections:
            # if connection != sender:
            await connection.send_text(message)
                # await connection.send_text(encrypted_message.decode())

    async def send_to_all(self, data: str):
        # encrypted_data = self.cipher_suite.encrypt(data.encode())
        for connection in self.active_connections:
            # if connection != sender:
            await connection.send_text(data)
                # await connection.send_text(encrypted_data.decode())


manager = WebSocketManager()


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_all(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    # finally:
    #     await websocket.close()



@app.post('/sendfile')
async def send_file(file_data: bytes):
    base64_data = base64.b64encode(file_data).decode('utf-8')
    # decoded_data = base64.b64decode(file_data)
    await manager.broadcast(base64_data)
    return {'message': 'File sent'}