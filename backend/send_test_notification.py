import requests
import json

def send_test_notification():
    notification_data = {
        "title": "Test Notification",
        "body": "This is a test notification from SmartProBono!"
    }

    try:
        response = requests.post(
            'http://localhost:5001/send-notification',
            json=notification_data
        )
        
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")

if __name__ == '__main__':
    send_test_notification()