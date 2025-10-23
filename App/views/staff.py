from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import (
    get_user_by_username,
    is_staff,
    create_staff,
    list_students,
    view_shortlists,
    view_internship_positions
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff', methods=['POST'])
def create_staff_route():
    data = request.json

    if get_user_by_username(data['username']):
        return jsonify({"error": "username already taken"}), 400

    staff = create_staff(data['username'], data['password'], data['email'])

    if staff is None:
        return jsonify({"error": "Failed to create staff"}), 400
    
    return jsonify({"message": "Staff account created", "staff_id": staff.id}), 201


@staff_views.route('/<staff_id>/internships', methods=['GET'])
@jwt_required()
def get_internships(staff_id):
    authenticated_staff_id = get_jwt_identity()
    
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 401
    
    result = view_internship_positions(staff_id)
    if result is None:
        return jsonify({"error": "Staff not found or database error"}), 404
    return jsonify(result), 200


@staff_views.route('/<staff_id>/students', methods=['GET'])
@jwt_required()
def get_students(staff_id):
    authenticated_staff_id = get_jwt_identity()
    
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 403
    
    result = list_students(staff_id)
    if result is None:
        return jsonify({"error": "Staff not found or database error"}), 404
    return jsonify(result), 200


@staff_views.route('/staff/<staff_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(staff_id):
    authenticated_staff_id = get_jwt_identity()
    
    if not is_staff(authenticated_staff_id):
        return jsonify({"error": "Access denied - staff authorization required"}), 403
    
    result = view_shortlists(staff_id)
    if result is None:
        return jsonify({"error": "Staff not found or database error"}), 404
    return jsonify(result), 200