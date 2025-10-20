from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, get_jwt_identity, get_jwt

from App.controllers import (
    create_staff,
    list_students,
    view_shortlists,
    view_internship_positions
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff', methods=['POST'])
def create_staff_view():
    data = request.json
    staff = create_staff(username=data['username'], password=data['password'], email=data['email'])
    
    try:
        return jsonify(staff.get_json()), 201
    except AttributeError:
        return jsonify({"error": staff}), 400


@staff_views.route('/<staff_id>/internships', methods=['GET'])
@jwt_required()
def get_internships(staff_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'staff':
        return jsonify({"error": "Access denied - staff credentials required"}), 403
    
    # Any staff can view all internships
    result = view_internship_positions(staff_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200


@staff_views.route('/<staff_id>/students', methods=['GET'])
@jwt_required()
def get_students(staff_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'staff':
        return jsonify({"error": "Access denied - staff authorization required"}), 403
    
    # Any staff can view all students
    result = list_students(staff_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200


@staff_views.route('/<staff_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(staff_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'staff':
        return jsonify({"error": "Access denied - staff authorization required"}), 403
    
    # Any staff can view all shortlists
    result = view_shortlists(staff_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200