#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Login"""
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage
from api.v1.views import app_views
import bcrypt


@app_views.route('/login', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/login_user.yml')
def login_user():
    """
    Login a user
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        abort(400, description="Missing email or password")
    
    # Fetch the user from the database
    user = storage.get_user_by_email(email.lower())
    
    if not user:
        abort(401, description="Incorrect email")
    
    # Check password validity
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = user.generate_auth_token()
        return jsonify({
            "message": "Successful login",
            "token": token
        }), 200
    
    else:
        abort(401, description="Incorrect Password")
