from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import is_staff, add_student_to_shortlist

shortlistEntry_views = Blueprint('shortlistEntry_views', __name__, template_folder='../templates')

@shortlistEntry_views.route('/shortlists/<shortlist_id>/students', methods=['POST'])
@jwt_required()
def add_student_to_shortlist_view(shortlist_id):
    staff_id = get_jwt_identity()
    
    if not is_staff(staff_id):
        return jsonify({"error": "Access denied - staff credentials required"}), 401
    
    student_id = request.json.get('student_id')
    
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400
    
    result = add_student_to_shortlist(staff_id, shortlist_id, student_id)
    
    if result:
        return jsonify({"message": f"Student {student_id} added to shortlist {shortlist_id}"}), 201
    return jsonify({"error": "Failed to add student - invalid IDs or student already exists"}), 400