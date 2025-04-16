import socketio
import time
import sys
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('websocket-test')

# Create a Socket.IO client
sio = socketio.Client(logger=True, engineio_logger=True)

# Event handler registration
@sio.event
def connect():
    logger.info("Connected to Socket.IO server!")
    print("\n✅ Connected to Socket.IO server!\n")

@sio.event
def connect_error(data):
    logger.error(f"Connection error: {data}")
    print(f"\n❌ Connection error: {data}\n")

@sio.event
def disconnect():
    logger.info("Disconnected from Socket.IO server")
    print("\n❌ Disconnected from server\n")

@sio.event
def connection_response(data):
    logger.info(f"Connection response: {data}")
    print(f"\n📩 Connection response: {json.dumps(data, indent=2)}\n")

@sio.event
def message_response(data):
    logger.info(f"Message response: {data}")
    print(f"\n📩 Message response: {json.dumps(data, indent=2)}\n")

@sio.event
def chat_update(data):
    logger.info(f"Chat update: {data}")
    print(f"\n📩 Chat update: {json.dumps(data, indent=2)}\n")

def main():
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = 'http://localhost:5002'
    
    print(f"\n🚀 Testing Socket.IO connection to {server_url}...")
    
    try:
        # Connect to the server with both transport options and public flag
        print("\n⏳ Attempting to connect... (This may take a few seconds)")
        sio.connect(
            f"{server_url}?public=true",
            transports=['websocket', 'polling'],
            wait_timeout=10,
            wait=True
        )
        
        print("\n📤 Sending test message...")
        sio.emit('message', 'Test message from Python client')
        
        print("\n📤 Sending test chat message...")
        sio.emit('chat_message', {
            'message': 'Hello from Python test client',
            'user': 'PythonTester',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
        })
        
        # Wait for responses
        print("\n⏳ Waiting for 5 seconds to receive responses...")
        time.sleep(5)
        
        # Disconnect
        print("\n👋 Disconnecting...")
        sio.disconnect()
        
        print("\n✅ Test completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error in Socket.IO test: {e}")
        print(f"\n❌ Error: {e}")
        
        # Provide debugging information
        print("\n🔍 Debugging information:")
        print("  - Make sure the Flask server is running")
        print("  - Check that the port is correct (default is 5002)")
        print("  - Verify that Socket.IO is properly configured in the server")
        print("  - Look for CORS issues if connecting from a different origin")
        print("  - Check if firewall is blocking connections")
        
        return 1

if __name__ == "__main__":
    sys.exit(main()) 