from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.OnboardingService import OnboardingService

bp = Blueprint('onboarding', __name__, url_prefix='/api/onboarding')

onboarding_service = OnboardingService()

@bp.route('', methods=['POST'])
@jwt_required()
def submit_onboarding():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No onboarding data provided'}), 400
        onboarding_service.processOnboarding(user_id, data)
        return jsonify({'success': True, 'message': 'Onboarding data saved.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 