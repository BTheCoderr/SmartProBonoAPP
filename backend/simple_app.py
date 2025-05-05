"""
Simple Flask application that doesn't depend on any of the problematic modules.
This is a backup solution for deployment.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'ok',
        'message': 'SmartProBono API is running in limited mode',
        'version': '1.0.0'
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'API health check successful',
        'version': '1.0.0'
    })

@app.route('/api/admin/health', methods=['GET'])
def admin_health():
    return jsonify({
        'status': 'ok',
        'message': 'Admin API health check successful',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 