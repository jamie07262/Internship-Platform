from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user, get_jwt

from.index import index_views
from App.models import db, Employer
from App.controllers import (create_internship_position)

internship_views = Blueprint('internship_views', __name__, template_folder='../templates')

@internship_views.route('/internships', methods=['POST'])
@jwt_required()
def create_internship():
    # Check user type from JWT claims
    claims = get_jwt()
    user_type = claims.get('user_type')
    
    if user_type != 'employer':
        return jsonify({"error": "Access denied - employer authorization required"}), 403
    
    employer_id = get_jwt_identity()
    employer = db.session.get(Employer, employer_id)

    if employer:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        duration = data.get('duration')
        
        if not all([title, description, duration]):
            return jsonify({"error": "title, description, and duration are required"}), 400
        
        internship = create_internship_position(
            employer_id=employer_id,
            title=title,
            description=description,
            duration=duration           
        )
        try:
            return jsonify(internship.get_json()), 201
        except AttributeError: 
            return jsonify({"error": internship}), 400
    
    return jsonify({"error": "Employer not found"}), 404