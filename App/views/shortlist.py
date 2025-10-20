from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from App.controllers import create_shortlist

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')


@shortlist_views.route('/shortlists', methods=['POST'])
@jwt_required()
def create_shortlist_route():
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'staff':
        return jsonify({"error": "Access denied - staff authorization required"}), 403
    
    staff_id = get_jwt_identity()
    data = request.json
    internship_id = data.get('internship_id')
    
    if not internship_id:
        return jsonify({"error": "internship_id is required"}), 400
    
    result = create_shortlist(staff_id, internship_id)
    
    try:
        return jsonify(result.get_json()), 201
    except AttributeError:  # result is a string, doesn't have get_json()
        return jsonify({"error": result}), 400