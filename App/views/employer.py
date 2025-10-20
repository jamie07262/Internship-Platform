from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user as get_jwt

from App.controllers import (
    create_employer,
    view_shortlist,
    accept_student,
    reject_student,
    get_jwt_identity
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')


@employer_views.route('/employer', methods=['POST'])
def create_employer():
    data = request.json
    employer = create_employer(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        companyName=data['companyName']
    )
    
    try:
        return jsonify(employer.get_json()), 201
    except AttributeError: 
        return jsonify({"error": employer}), 400


@employer_views.route('/<employer_id>/shortlists', methods=['GET'])
@jwt_required()
def get_shortlists(employer_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'employer':
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    # Verify the employer can only access their own shortlists
    authenticated_employer_id = get_jwt_identity()
    if authenticated_employer_id != employer_id:
        return jsonify({"error": "Access denied - can only view your own shortlists"}), 403
    
    result = view_shortlist(employer_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200


@employer_views.route('/internships/<internship_id>/accept/<student_id>', methods=['PUT'])
@jwt_required()
def accept_student_route(internship_id, student_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'employer':
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    employer_id = get_jwt_identity()
    result = accept_student(employer_id, internship_id, student_id)
    
    # Check if result contains success indicators
    if "accepted" in result.lower() and "error" not in result.lower():
        return jsonify({"message": result}), 200
    return jsonify({"error": result}), 400


@employer_views.route('/internships/<internship_id>/reject/<student_id>', methods=['PUT'])
@jwt_required()
def reject_student_route(internship_id, student_id):
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'employer':
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    employer_id = get_jwt_identity()
    result = reject_student(employer_id, internship_id, student_id)
    
    # Check if result contains success indicators
    if "rejected" in result.lower() and "error" not in result.lower():
        return jsonify({"message": result}), 200
    return jsonify({"error": result}), 400