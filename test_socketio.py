import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to Socket.IO server!")
    # Send a test message after connecting
    sio.emit('message', 'Hello from Python Socket.IO client!')

@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")

@sio.event
def connection_response(data):
    print(f"Got connection response: {data}")

@sio.event
def message_response(data):
    print(f"Got message response: {data}")

@sio.event
def chat_update(data):
    print(f"Got chat update: {data}")

def main():
    try:
        print("Connecting to Socket.IO server...")
        sio.connect('http://localhost:5002')
        
        # Keep the script running for a bit to receive responses
        print("Waiting for messages...")
        time.sleep(2)
        
        # Send a chat message
        print("Sending a chat message...")
        sio.emit('chat_message', {
            'message': 'Hello from Python chat!',
            'user': 'Python Test Client',
            'timestamp': time.time()
        })
        
        # Wait for responses
        time.sleep(5)
        
        # Disconnect
        sio.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 