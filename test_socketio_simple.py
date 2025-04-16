import socketio
import time
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('socketio')
logger.setLevel(logging.DEBUG)

# Create a Socket.IO client
sio = socketio.Client(logger=True, engineio_logger=True)

# Define event handlers
@sio.event
def connect():
    print("Connected to server!")

@sio.event
def connect_error(data):
    print(f"Connection error: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")

# Main execution
if __name__ == "__main__":
    try:
        print("Connecting to Socket.IO server at http://localhost:5002...")
        sio.connect('http://localhost:5002', 
                    transports=['websocket', 'polling'],
                    wait_timeout=10)
        
        print("Sending test message...")
        sio.emit('message', 'Test message from Python client')
        
        # Keep the program running
        try:
            print("Press Ctrl+C to exit...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            sio.disconnect()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 