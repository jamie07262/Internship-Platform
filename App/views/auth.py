from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt

from.index import index_views

from App.controllers.auth import jwt_authenticate, login

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify(error='Username and password are required'), 400

    token = jwt_authenticate(data['username'], data['password'])
    if not token:
        return jsonify(error='Invalid credentials'), 401
    
    return jsonify(access_token=token), 200 

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify():
    try:
        claims = get_jwt()
        user_id = get_jwt_identity()  # Now gets just the user ID
        username = claims.get('username')  # From additional_claims
        user_type = claims.get('user_type', 'unknown')  # From additional_claims
        
        return jsonify({
            'user_id': user_id,
            'username': username,
            'user_type': user_type,
            'message': f'Logged in as {username} ({user_type})'
        }), 200
    except Exception as e:
        return jsonify(error='Unable to identify user'), 401

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

# '''
# API Routes
# '''

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
#   data = request.json
#   token = login(data['username'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   response = jsonify(access_token=token) 
#   set_access_cookies(response, token)
#   return response

# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user():
#     return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

# @auth_views.route('/api/logout', methods=['GET'])
# def logout_api():
#     response = jsonify(message="Logged Out!")
#     unset_jwt_cookies(response)
#     return response