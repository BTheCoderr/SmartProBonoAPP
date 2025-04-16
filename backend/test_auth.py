"""
Simple test script to authenticate a user with the WebSocket
"""
import socketio
import time
import sys
import logging
import signal

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('socketio')
logger.setLevel(logging.DEBUG)

# Create a Socket.IO client
sio = socketio.Client(logger=True, engineio_logger=True)

# Flag to control the main loop
keep_running = True

# Event handlers
@sio.event
def connect():
    print("Connected to server!")
    # Authenticate with hardcoded user ID
    print("Authenticating with user ID 1...")
    sio.emit('authenticate', {'user_id': 1})

@sio.event
def connect_error(data):
    print(f"Connection error: {data}")
    sys.exit(1)

@sio.event
def disconnect():
    print("Disconnected from server")
    global keep_running
    keep_running = False

@sio.event
def connection_success(data):
    print(f"Connection success: {data}")

@sio.event
def auth_success(data):
    print(f"Authentication success: {data}")
    print("User is now authenticated! Check the /api/connections endpoint.")
    print("Keeping connection open until Ctrl+C is pressed...")

@sio.event
def auth_error(data):
    print(f"Authentication error: {data}")
    sio.disconnect()
    sys.exit(1)

# Add handlers for additional events for debugging
@sio.event
def notification(data):
    print(f"Received notification: {data}")

@sio.event
def message(data):
    print(f"Received message: {data}")

@sio.event
def error(data):
    print(f"Received error: {data}")

def signal_handler(sig, frame):
    """Handle Ctrl+C signal"""
    print('\nCtrl+C pressed. Exiting...')
    global keep_running
    keep_running = False
    sio.disconnect()
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        print("Connecting to Socket.IO server at http://localhost:5002...")
        sio.connect('http://localhost:5002', 
                    transports=['websocket', 'polling'],
                    wait_timeout=10)
        
        # Keep the connection open indefinitely until Ctrl+C
        counter = 0
        while keep_running:
            time.sleep(1)
            counter += 1
            if counter % 60 == 0:  # Log every minute
                print(f"Still connected... ({counter} seconds)")
            
        print("Disconnecting...")
        sio.disconnect()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 