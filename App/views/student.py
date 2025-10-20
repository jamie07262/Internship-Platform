from unittest import result
from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from App.controllers import ( create_student, view_my_shortlists)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student', methods=['POST'])
def create_student():
    data = request.json
    student = create_student(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        skills=data['skills']
    )
    try:
        return jsonify(student.get_json()), 201
    except AttributeError:
        return jsonify({"error": student}), 400


@student_views.route('/<student_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(student_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'student':
        return jsonify({"error": "Access denied - student credentials required"}), 403
    
    # Verify student can only access their own shortlists
    authenticated_student_id = get_jwt_identity()
    if authenticated_student_id != student_id:
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 403
    
    result = view_my_shortlists(student_id)

    try:
        return jsonify(result.get_json()), 200
    except AttributeError:
        return jsonify({"error": result}), 404