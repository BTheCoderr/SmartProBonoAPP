import socketio
import time
import json
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('socketio')
logger.setLevel(logging.DEBUG)

# Create a Socket.IO client
sio = socketio.Client()

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

@sio.event
def connection_success(data):
    print(f"Connection success: {data}")
    
    # Authenticate with the server
    user_id = input("Enter user ID to authenticate: ")
    sio.emit('authenticate', {'user_id': user_id})

@sio.event
def auth_success(data):
    print(f"Authentication success: {data}")
    print("\nOptions:")
    print("1. Send test notification")
    print("2. Exit")
    choice = input("Enter choice: ")
    
    if choice == '1':
        title = input("Enter notification title: ")
        message = input("Enter notification message: ")
        notification_type = input("Enter notification type (info, success, warning, error): ")
        
        sio.emit('test_notification', {
            'title': title,
            'message': message,
            'type': notification_type
        })
    elif choice == '2':
        sio.disconnect()
        sys.exit(0)

@sio.event
def auth_error(data):
    print(f"Authentication error: {data}")
    sio.disconnect()
    sys.exit(1)

@sio.event
def notification(data):
    print("\n===== New Notification =====")
    print(f"Title: {data.get('title')}")
    print(f"Message: {data.get('message')}")
    print(f"Type: {data.get('type')}")
    print(f"Time: {data.get('created_at')}")
    print(f"Read: {data.get('is_read')}")
    print("============================\n")

@sio.event
def success(data):
    print(f"Success: {data}")
    
    print("\nOptions:")
    print("1. Send another test notification")
    print("2. Exit")
    choice = input("Enter choice: ")
    
    if choice == '1':
        title = input("Enter notification title: ")
        message = input("Enter notification message: ")
        notification_type = input("Enter notification type (info, success, warning, error): ")
        
        sio.emit('test_notification', {
            'title': title,
            'message': message,
            'type': notification_type
        })
    elif choice == '2':
        sio.disconnect()
        sys.exit(0)

@sio.event
def error(data):
    print(f"Error: {data}")

# Main execution
if __name__ == "__main__":
    try:
        print("Connecting to Socket.IO server at http://localhost:5002...")
        sio.connect('http://localhost:5002', 
                    transports=['websocket', 'polling'],
                    wait_timeout=10)
        
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