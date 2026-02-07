from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter(tags=["Chat"])

# 1. THE MANAGER
# This class handles all the active connections.
class ConnectionManager:
    def __init__(self):
        # Dictionary to hold active connections: { "room_name": [connection1, connection2] }
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if room_name not in self.active_connections:
            self.active_connections[room_name] = []
        self.active_connections[room_name].append(websocket)

    def disconnect(self, websocket: WebSocket, room_name: str):
        if room_name in self.active_connections:
            self.active_connections[room_name].remove(websocket)
            if not self.active_connections[room_name]:
                del self.active_connections[room_name]

    async def broadcast(self, message: str, room_name: str):
        # Send the message to everyone in the room
        if room_name in self.active_connections:
            for connection in self.active_connections[room_name]:
                await connection.send_text(message)

manager = ConnectionManager()

# 2. THE WEBSOCKET ENDPOINT
# URL will look like: ws://localhost:8000/ws/goa/piyush
@router.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, user_name: str):
    await manager.connect(websocket, room_name)
    
    # Notify others that user joined
    await manager.broadcast(f"🟢 {user_name} joined the chat!", room_name)
    
    try:
        while True:
            # Wait for user to send a message
            data = await websocket.receive_text()
            # Broadcast it to everyone
            await manager.broadcast(f"{user_name}: {data}", room_name)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_name)
        await manager.broadcast(f"🔴 {user_name} left the chat.", room_name)