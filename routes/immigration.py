from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from models import User
import uuid  # Add this for generating mock IDs

immigration = Blueprint('immigration', __name__, url_prefix='/api/immigration')

# Simple test route
@immigration.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Immigration API test route is working"}), 200

# Role-based access control decorator
def lawyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Get JWT claims
        claims = get_jwt()
        role = claims.get('role', '')
        
        # Check if user has lawyer or admin role
        if role not in ['lawyer', 'admin']:
            return jsonify({'error': 'Access denied. Lawyer or admin rights required.'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

# Mock data storage for testing purposes
mock_immigration_intake = []
mock_cases = [] 