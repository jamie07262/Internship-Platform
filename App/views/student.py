from unittest import result
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import ( get_user_by_username, is_student, create_student, view_my_shortlists)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student', methods=['POST'])
def create_student_route():
    data = request.json

    if get_user_by_username(data['username']):
        return jsonify({"error": "username already taken"}), 400
    
    student = create_student(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        skills=data['skills']
    )

    if student is None:
        return jsonify({"error": "Failed to create student"}), 400
    return jsonify({"message": "Student account created", "student_id": student.id}), 201


@student_views.route('/student/<student_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(student_id):
    authenticated_student_id = get_jwt_identity()
    
    if not is_student(authenticated_student_id):
        return jsonify({"error": "Access denied - student credentials required"}), 401
    
    # Verify student can only access their own shortlists
    if str(authenticated_student_id) != str(student_id):
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 401
    
    result = view_my_shortlists(student_id)

    if result is None:
        return jsonify({"error": "Student not found or database error"}), 404
    return jsonify(result), 200