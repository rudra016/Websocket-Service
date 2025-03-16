from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept and maintain the WebSocket connection."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected.")

        try:
            while True:
                await websocket.receive_text()  # Keeps connection alive
        except WebSocketDisconnect:
            self.disconnect(user_id)
            print(f"User {user_id} disconnected.")

    def disconnect(self, user_id: int):
        """Handle user disconnection."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} removed from active connections.")

    async def send_order_update(self, user_id: int, message: str):
        """Send real-time updates if user is connected."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
            except Exception as e:
                print(f"Error sending WebSocket message to user {user_id}: {e}")

websocket_manager = WebSocketManager()
