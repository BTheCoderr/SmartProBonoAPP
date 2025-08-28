"""Beta signup routes for Flask"""
import logging
import secrets
from datetime import datetime
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError
from routes import beta_bp
from database import db
from models.beta_signup import BetaSignup
from services.email_service import send_confirmation_email_flask, send_subscription_confirmation
from services.analytics_service import track_event_flask

logger = logging.getLogger(__name__)

@beta_bp.route('/signup', methods=['POST'])
def beta_signup():
    """Handle beta signup requests with email confirmation."""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400
            
        email = data['email']
        source = data.get('source')
        utm_source = data.get('utm_source')
        utm_medium = data.get('utm_medium')
        utm_campaign = data.get('utm_campaign')
        
        # Generate confirmation token
        confirmation_token = secrets.token_urlsafe(32)
        
        # Create new signup record
        db_signup = BetaSignup(
            email=email,
            source=source,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            confirmation_token=confirmation_token
        )
        
        db.session.add(db_signup)
        db.session.commit()
        
        # Send confirmation email
        send_confirmation_email_flask(
            to_email=email,
            confirmation_token=confirmation_token
        )
        
        # Track signup event
        track_event_flask(
            event_name="beta_signup",
            properties={
                "email": email,
                "source": source,
                "utm_source": utm_source,
                "utm_medium": utm_medium,
                "utm_campaign": utm_campaign,
                "ip_address": request.remote_addr
            }
        )
        
        return jsonify({
            "status": "success",
            "message": "Please check your email to confirm your signup."
        })
        
    except Exception as e:
        logger.error(f"Beta signup error: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to process beta signup"}), 500

@beta_bp.route('/confirm/<token>', methods=['GET'])
def confirm_signup(token):
    """Confirm beta signup email."""
    try:
        signup = BetaSignup.query.filter_by(
            confirmation_token=token,
            is_confirmed=False
        ).first()
        
        if not signup:
            return jsonify({"error": "Invalid or expired confirmation token"}), 404
        
        # Update signup record
        signup.is_confirmed = True
        signup.confirmed_at = datetime.now()
        signup.confirmation_token = None  # Invalidate token
        
        db.session.commit()
        
        # Track confirmation event
        track_event_flask(
            event_name="beta_signup_confirmed",
            properties={"email": signup.email}
        )
        
        return jsonify({
            "status": "success",
            "message": "Thank you for confirming your email! We'll notify you when the beta is ready."
        })
        
    except Exception as e:
        logger.error(f"Beta confirmation error: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to confirm signup"}), 500

@beta_bp.route('/subscribe', methods=['POST'])
def subscribe_email():
    """Handle email subscription preferences"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400
            
        email = data['email']
        preferences = data.get('preferences', {})
        
        # Validate preferences
        valid_preferences = {
            'productUpdates': preferences.get('productUpdates', False),
            'legalNews': preferences.get('legalNews', False),
            'tips': preferences.get('tips', False)
        }
        
        # Check if any preferences are selected
        if not any(valid_preferences.values()):
            return jsonify({"error": "At least one subscription type must be selected"}), 400
        
        # Store subscription in database
        from services.email_service import send_subscription_confirmation
        
        # Find user by email (existing signup or confirmed user)
        signup = BetaSignup.query.filter_by(email=email).first()
        
        if signup:
            # Update preferences for existing user
            signup.subscription_preferences = valid_preferences
            signup.subscribed_at = datetime.now()
            db.session.commit()
        else:
            # Create a new subscription record
            db_subscription = BetaSignup(
                email=email,
                subscription_preferences=valid_preferences,
                subscribed_at=datetime.now(),
                source='email_subscription'
            )
            db.session.add(db_subscription)
            db.session.commit()
        
        # Send confirmation email
        send_subscription_confirmation(email, valid_preferences)
        
        # Track subscription event
        track_event_flask(
            event_name="email_subscription",
            properties={
                "email": email,
                "preferences": valid_preferences
            }
        )
        
        return jsonify({
            "status": "success",
            "message": "Successfully subscribed to updates!"
        })
        
    except Exception as e:
        logger.error(f"Email subscription error: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to process subscription"}), 500 