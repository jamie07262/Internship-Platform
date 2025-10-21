from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from App.controllers import create_shortlist, internship, is_staff
from App.models.shortlist import Shortlist

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')


@shortlist_views.route('/shortlists', methods=['POST'])
@jwt_required()
def create_shortlist_route():
    staff_id = get_jwt_identity()
    
    if not is_staff(staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    data = request.json
    internship_id = data.get('internship_id')
    
    if not internship_id:
        return jsonify({"error": "correct internship_id is required"}), 400
    
    result = create_shortlist(staff_id, internship_id)
    
    if not isinstance(result, Shortlist):
        if str(result) == "duplicate shortlist":
            return jsonify({"error": "Duplicate shortlist"}), 500
        else:
            return jsonify({"error": result}), 400
    return jsonify({"message": "shortlist created"}), 201