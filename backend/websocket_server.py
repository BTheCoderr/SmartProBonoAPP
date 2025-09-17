"""
WebSocket Server for Real-Time Features
Handles real-time notifications, live chat, and document collaboration
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
import uuid

try:
    from websockets import WebSocketServerProtocol, serve
    from websockets.exceptions import ConnectionClosed
except ImportError:
    print("WebSocket support not available. Install with: pip install websockets")
    WebSocketServerProtocol = None

logger = logging.getLogger(__name__)

@dataclass
class WebSocketMessage:
    """Represents a WebSocket message"""
    message_id: str
    message_type: str  # 'notification', 'chat', 'document_update', 'case_update'
    data: Dict[str, Any]
    timestamp: str
    sender_id: Optional[str] = None
    recipient_id: Optional[str] = None
    room_id: Optional[str] = None

@dataclass
class ClientConnection:
    """Represents a connected client"""
    websocket: WebSocketServerProtocol
    client_id: str
    user_id: Optional[str]
    user_type: str  # 'client', 'lawyer', 'bondsman', 'admin'
    rooms: Set[str]
    last_activity: datetime

class WebSocketManager:
    """Manages WebSocket connections and real-time features"""
    
    def __init__(self):
        self.clients: Dict[str, ClientConnection] = {}
        self.rooms: Dict[str, Set[str]] = {}  # room_id -> set of client_ids
        self.message_history: List[WebSocketMessage] = []
        self.max_history = 1000
        
    def add_client(self, websocket: WebSocketServerProtocol, client_id: str, user_id: Optional[str] = None, user_type: str = "client") -> ClientConnection:
        """Add a new client connection"""
        connection = ClientConnection(
            websocket=websocket,
            client_id=client_id,
            user_id=user_id,
            user_type=user_type,
            rooms=set(),
            last_activity=datetime.now()
        )
        self.clients[client_id] = connection
        logger.info(f"Client {client_id} connected")
        return connection
    
    def remove_client(self, client_id: str):
        """Remove a client connection"""
        if client_id in self.clients:
            connection = self.clients[client_id]
            
            # Remove from all rooms
            for room_id in connection.rooms:
                if room_id in self.rooms:
                    self.rooms[room_id].discard(client_id)
                    if not self.rooms[room_id]:
                        del self.rooms[room_id]
            
            del self.clients[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    def join_room(self, client_id: str, room_id: str) -> bool:
        """Add client to a room"""
        if client_id not in self.clients:
            return False
        
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        
        self.rooms[room_id].add(client_id)
        self.clients[client_id].rooms.add(room_id)
        logger.info(f"Client {client_id} joined room {room_id}")
        return True
    
    def leave_room(self, client_id: str, room_id: str) -> bool:
        """Remove client from a room"""
        if client_id not in self.clients:
            return False
        
        if room_id in self.rooms:
            self.rooms[room_id].discard(client_id)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
        
        self.clients[client_id].rooms.discard(room_id)
        logger.info(f"Client {client_id} left room {room_id}")
        return True
    
    async def send_to_client(self, client_id: str, message: WebSocketMessage) -> bool:
        """Send message to specific client"""
        if client_id not in self.clients:
            return False
        
        try:
            connection = self.clients[client_id]
            await connection.websocket.send(json.dumps(asdict(message)))
            connection.last_activity = datetime.now()
            return True
        except ConnectionClosed:
            self.remove_client(client_id)
            return False
        except Exception as e:
            logger.error(f"Error sending message to client {client_id}: {e}")
            return False
    
    async def send_to_room(self, room_id: str, message: WebSocketMessage) -> int:
        """Send message to all clients in a room"""
        if room_id not in self.rooms:
            return 0
        
        sent_count = 0
        for client_id in list(self.rooms[room_id]):  # Create a copy to avoid modification during iteration
            if await self.send_to_client(client_id, message):
                sent_count += 1
        
        return sent_count
    
    async def broadcast(self, message: WebSocketMessage) -> int:
        """Broadcast message to all connected clients"""
        sent_count = 0
        for client_id in list(self.clients.keys()):
            if await self.send_to_client(client_id, message):
                sent_count += 1
        
        return sent_count
    
    def create_message(self, message_type: str, data: Dict[str, Any], sender_id: Optional[str] = None, recipient_id: Optional[str] = None, room_id: Optional[str] = None) -> WebSocketMessage:
        """Create a new WebSocket message"""
        return WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            data=data,
            timestamp=datetime.now().isoformat(),
            sender_id=sender_id,
            recipient_id=recipient_id,
            room_id=room_id
        )
    
    def add_to_history(self, message: WebSocketMessage):
        """Add message to history"""
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history = self.message_history[-self.max_history:]
    
    def get_room_history(self, room_id: str, limit: int = 50) -> List[WebSocketMessage]:
        """Get message history for a room"""
        room_messages = [msg for msg in self.message_history if msg.room_id == room_id]
        return room_messages[-limit:]
    
    def get_client_stats(self) -> Dict[str, Any]:
        """Get statistics about connected clients"""
        return {
            "total_clients": len(self.clients),
            "total_rooms": len(self.rooms),
            "clients_by_type": {
                user_type: len([c for c in self.clients.values() if c.user_type == user_type])
                for user_type in ["client", "lawyer", "bondsman", "admin"]
            },
            "active_rooms": list(self.rooms.keys())
        }

# Global WebSocket manager
ws_manager = WebSocketManager()

async def handle_websocket_connection(websocket: WebSocketServerProtocol, path: str):
    """Handle new WebSocket connection"""
    client_id = str(uuid.uuid4())
    connection = ws_manager.add_client(websocket, client_id)
    
    try:
        # Send welcome message
        welcome_message = ws_manager.create_message(
            message_type="connection",
            data={
                "status": "connected",
                "client_id": client_id,
                "server_time": datetime.now().isoformat()
            }
        )
        await ws_manager.send_to_client(client_id, welcome_message)
        
        async for message in websocket:
            try:
                data = json.loads(message)
                await handle_client_message(client_id, data)
            except json.JSONDecodeError:
                error_message = ws_manager.create_message(
                    message_type="error",
                    data={"error": "Invalid JSON format"}
                )
                await ws_manager.send_to_client(client_id, error_message)
            except Exception as e:
                logger.error(f"Error handling message from client {client_id}: {e}")
                error_message = ws_manager.create_message(
                    message_type="error",
                    data={"error": "Internal server error"}
                )
                await ws_manager.send_to_client(client_id, error_message)
    
    except ConnectionClosed:
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection {client_id}: {e}")
    finally:
        ws_manager.remove_client(client_id)

async def handle_client_message(client_id: str, data: Dict[str, Any]):
    """Handle incoming message from client"""
    message_type = data.get("type")
    
    if message_type == "join_room":
        room_id = data.get("room_id")
        if room_id:
            ws_manager.join_room(client_id, room_id)
            response = ws_manager.create_message(
                message_type="room_joined",
                data={"room_id": room_id, "client_id": client_id}
            )
            await ws_manager.send_to_client(client_id, response)
    
    elif message_type == "leave_room":
        room_id = data.get("room_id")
        if room_id:
            ws_manager.leave_room(client_id, room_id)
            response = ws_manager.create_message(
                message_type="room_left",
                data={"room_id": room_id, "client_id": client_id}
            )
            await ws_manager.send_to_client(client_id, response)
    
    elif message_type == "chat_message":
        room_id = data.get("room_id")
        message_text = data.get("message", "")
        
        if room_id and message_text:
            chat_message = ws_manager.create_message(
                message_type="chat",
                data={
                    "message": message_text,
                    "sender": data.get("sender", "Anonymous"),
                    "client_id": client_id
                },
                sender_id=client_id,
                room_id=room_id
            )
            ws_manager.add_to_history(chat_message)
            await ws_manager.send_to_room(room_id, chat_message)
    
    elif message_type == "document_update":
        room_id = data.get("room_id")
        document_data = data.get("document_data", {})
        
        if room_id:
            doc_message = ws_manager.create_message(
                message_type="document_update",
                data={
                    "document_id": data.get("document_id"),
                    "changes": document_data,
                    "client_id": client_id
                },
                sender_id=client_id,
                room_id=room_id
            )
            ws_manager.add_to_history(doc_message)
            await ws_manager.send_to_room(room_id, doc_message)
    
    elif message_type == "get_history":
        room_id = data.get("room_id")
        limit = data.get("limit", 50)
        
        if room_id:
            history = ws_manager.get_room_history(room_id, limit)
            history_message = ws_manager.create_message(
                message_type="history",
                data={
                    "room_id": room_id,
                    "messages": [asdict(msg) for msg in history]
                }
            )
            await ws_manager.send_to_client(client_id, history_message)
    
    elif message_type == "get_stats":
        stats = ws_manager.get_client_stats()
        stats_message = ws_manager.create_message(
            message_type="stats",
            data=stats
        )
        await ws_manager.send_to_client(client_id, stats_message)

async def send_notification(notification_type: str, data: Dict[str, Any], recipient_id: Optional[str] = None, room_id: Optional[str] = None):
    """Send a notification to clients"""
    message = ws_manager.create_message(
        message_type="notification",
        data={
            "notification_type": notification_type,
            "data": data
        },
        recipient_id=recipient_id,
        room_id=room_id
    )
    
    if recipient_id:
        await ws_manager.send_to_client(recipient_id, message)
    elif room_id:
        await ws_manager.send_to_room(room_id, message)
    else:
        await ws_manager.broadcast(message)

async def send_case_update(case_id: str, update_data: Dict[str, Any], user_id: Optional[str] = None):
    """Send case update notification"""
    message = ws_manager.create_message(
        message_type="case_update",
        data={
            "case_id": case_id,
            "update": update_data
        },
        recipient_id=user_id
    )
    
    if user_id:
        await ws_manager.send_to_client(user_id, message)
    else:
        await ws_manager.broadcast(message)

async def start_websocket_server(host: str = "localhost", port: int = 8765):
    """Start the WebSocket server"""
    if WebSocketServerProtocol is None:
        logger.error("WebSocket support not available. Install with: pip install websockets")
        return
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with serve(handle_websocket_connection, host, port):
        logger.info(f"WebSocket server running on ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Start the server
    asyncio.run(start_websocket_server())
