from typing import Dict, Optional
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
from datetime import datetime

class WebSocketService:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.setup_handlers()

    def setup_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            print(f"Client connected: {request.sid}")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            print(f"Client disconnected: {request.sid}")

        @self.socketio.on('join')
        def handle_join(data):
            """Handle client joining a room."""
            user_id = data.get('user_id')
            if user_id:
                join_room(f"user_{user_id}")
                print(f"User {user_id} joined their room")

        @self.socketio.on('leave')
        def handle_leave(data):
            """Handle client leaving a room."""
            user_id = data.get('user_id')
            if user_id:
                leave_room(f"user_{user_id}")
                print(f"User {user_id} left their room")

    def emit_to_user(self, user_id: str, event: str, data: Dict):
        """Emit an event to a specific user's room."""
        room = f"user_{user_id}"
        self.socketio.emit(event, data, room=room)

    def broadcast_notification(self, user_id: str, notification: Dict):
        """Broadcast a notification to a specific user."""
        notification["timestamp"] = datetime.utcnow().isoformat()
        self.emit_to_user(user_id, "notification", notification)

    def broadcast_document_update(self, user_id: str, document_data: Dict):
        """Broadcast a document update to a specific user."""
        self.emit_to_user(user_id, "document_update", document_data)

    def broadcast_system_message(self, message: str, user_id: Optional[str] = None):
        """Broadcast a system message to all users or a specific user."""
        data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        if user_id:
            self.emit_to_user(user_id, "system_message", data)
        else:
            self.socketio.emit("system_message", data)

# Note: Don't create instance here - it needs the SocketIO instance from app.py 