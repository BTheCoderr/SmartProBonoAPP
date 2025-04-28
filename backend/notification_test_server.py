from flask import Flask, jsonify, request
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)

# Store subscriptions in memory (in production, use a database)
subscriptions = []

# Load VAPID keys
with open('vapid_keys.json', 'r') as f:
    vapid_keys = json.load(f)

VAPID_PRIVATE_KEY = vapid_keys['private_key']
VAPID_PUBLIC_KEY = vapid_keys['public_key']
VAPID_CLAIMS = {
    "sub": "mailto:test@example.com"
}

@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription = request.json
    if subscription not in subscriptions:
        subscriptions.append(subscription)
    return jsonify({'success': True})

@app.route('/send-notification', methods=['POST'])
def send_notification():
    try:
        data = request.json
        notification_data = {
            "title": data.get("title", "Test Notification"),
            "body": data.get("body", "This is a test notification"),
            "icon": "/logo192.png"
        }

        for subscription in subscriptions:
            try:
                webpush(
                    subscription_info=subscription,
                    data=json.dumps(notification_data),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims=VAPID_CLAIMS
                )
            except WebPushException as e:
                print(f"Subscription failed: {str(e)}")
                if e.response and e.response.status_code == 410:
                    subscriptions.remove(subscription)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/vapid-public-key')
def get_vapid_public_key():
    return jsonify({'publicKey': VAPID_PUBLIC_KEY})

if __name__ == '__main__':
    app.run(port=5001, debug=True) 