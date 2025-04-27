from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import secrets
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_mail import Mail
from logging.handlers import RotatingFileHandler
import eventlet
from flask_socketio import SocketIO

# Patch eventlet for SocketIO to work correctly
eventlet.monkey_patch()

# Import database modules
from database import db, migrate, init_db

# Import SocketIO setup 
from websocket.core import socketio, init_websocket
from routes.test import test_bp
from routes.immigration_notifications import immigration_notifications_bp

# Import notification routes
from routes.notification import notification_bp 