from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from App.controllers import (
    is_employer,
    get_user_by_username,
    create_employer,
    view_shortlist,
    accept_student,
    reject_student,
    get_jwt_identity
)
employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/employer', methods=['POST'])
def create_employer_route():
    data = request.json

    if get_user_by_username(data['username']):
        return jsonify({"error": "username already taken"}), 400
    
    employer = create_employer(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        companyName=data['companyName']
    )
    
    if employer is None:
        return jsonify({"error": "Failed to create employer"}), 400
    return jsonify({"message": "Employer account created", "employer_id": employer.id}), 201


@employer_views.route('/employer/<employer_id>/shortlists', methods=['GET'])
@jwt_required()
def emp_get_shortlists(employer_id):
    
    authenticated_employer_id = get_jwt_identity()

    if not is_employer(authenticated_employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401

    if str(authenticated_employer_id) != str(employer_id):
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 401

    result = view_shortlist(int(employer_id))
    
    if result is None:
        return jsonify({"error": "Employer not found or database error"}), 404
    return jsonify(result), 200


@employer_views.route('/internships/<internship_id>/students/<student_id>/accept', methods=['PUT'])
@jwt_required()
def accept_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401
    
    result = accept_student(employer_id, internship_id, student_id)

    if result:
        return jsonify({"message": f"Student ID {student_id} has been accepted"}), 200
    return jsonify({"error": "Failed to accept student - invalid IDs or student not in shortlist"}), 400


@employer_views.route('/internships/<internship_id>/students/<student_id>/reject', methods=['PUT'])
@jwt_required()
def reject_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401
    
    result = reject_student(employer_id, internship_id, student_id)

    if result:
        return jsonify({"message": f"Student ID {student_id} has been rejected"}), 200
    return jsonify({"error": "Failed to reject student - invalid IDs or student not in shortlist"}), 400