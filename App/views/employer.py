from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user as get_jwt

from App.controllers import (
    is_employer,
    get_user_by_username,
    create_employer,
    view_shortlist,
    accept_student,
    reject_student,
    get_jwt_identity
)
from App.models.employer import Employer

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
    
    if not isinstance(employer, Employer):
        return jsonify({"error": employer}), 400

    return jsonify({"message": "account created", "employer_id": employer.id}), 201


@employer_views.route('/<employer_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(employer_id):
    
    authenticated_employer_id = get_jwt_identity()

    if not is_employer(authenticated_employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    if authenticated_employer_id != employer_id:
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 403
    
    result = view_shortlist(employer_id)

    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200


@employer_views.route('/internships/<internship_id>/accept/<student_id>', methods=['PUT'])
@jwt_required()
def accept_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    result = accept_student(employer_id, internship_id, student_id)
    
    if result == "accepted":
        return jsonify({"message": f"Student ID {student_id} has been accepted by employer ID {employer_id}."}), 200
    return jsonify({"error": "Failed to accept student"}), 400


@employer_views.route('/internships/<internship_id>/reject/<student_id>', methods=['PUT'])
@jwt_required()
def reject_student_route(internship_id, student_id):
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    result = reject_student(employer_id, internship_id, student_id)
       
    if result == "rejected":
        return jsonify({"message": f"Student ID {student_id} has been rejected by employer ID {employer_id}"}), 200
    return jsonify({"error": "Failed to reject student"}), 400