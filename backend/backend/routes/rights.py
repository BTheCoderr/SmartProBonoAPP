from flask import Blueprint, jsonify, request, current_app
from models.rights import Rights
from database import db

bp = Blueprint('rights', __name__)

@bp.route('/api/rights', methods=['GET'])
def get_rights():
    rights = Rights.query.all()
    return jsonify([right.to_dict() for right in rights])

@bp.route('/api/rights/<category>', methods=['GET'])
def get_rights_by_category(category):
    rights = Rights.query.filter_by(category=category).all()
    return jsonify([right.to_dict() for right in rights])

@bp.route('/api/rights/<int:right_id>', methods=['GET'])
def get_right(right_id):
    right = Rights.query.get_or_404(right_id)
    return jsonify(right.to_dict())