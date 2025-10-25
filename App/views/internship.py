from flask import Blueprint,jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from App.models import Internship
from App.controllers import (create_internship_position, is_employer)

internship_views = Blueprint('internship_views', __name__, template_folder='../templates')

@internship_views.route('/internships', methods=['POST'])
@jwt_required()
def create_internship():
    employer_id = get_jwt_identity()
    
    if not is_employer(employer_id):
        return jsonify({"error": "Access denied - employer authorization required"}), 401
    

    data = request.json
    title = data.get('title')
    description = data.get('description')
    duration = data.get('duration')

    if not all([title and title.strip(), description and description.strip(), duration]):
        return jsonify({"error": "title, description, and duration are required and cannot be empty"}), 400
    
    internship = create_internship_position(
        employer_id=employer_id,
        title=title,
        description=description,
        duration=duration           
    )
    
    if not isinstance(internship, Internship):
        if "exists" in str(internship).lower():
            return jsonify({"error": "Duplicate internship: You cannot create an internship with the same title, description, and duration"}), 500
        else:
            return jsonify({"error": internship}), 400       

    return jsonify({
        "message": f"Internship created by employer ID {employer_id}",
        "internship_id": internship.id
    }), 201