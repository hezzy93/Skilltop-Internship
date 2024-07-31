#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Reset password"""
from os import getenv
from dotenv import load_dotenv
from flask import request, jsonify, abort, url_for
from flasgger.utils import swag_from
from models import storage
from models.reset_password import ResetPassword
from api.v1.views import app_views
from api.v1.email import send_email  # Import the asynchronous send_email function


# Load environment variables from .env file
load_dotenv()


# Router to reset password
@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/reset_password.yml')
def reset_password():
    """
    Send a password reset link to the user's email
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        abort(400, description="Missing email")
    
    # Fetch the user from the database
    user = storage.get_user_by_email(email.lower())  # Ensure email is lowercased
    
    if not user:
        abort(404, description="User not found")
    
    # Generate a password reset token
    token = ResetPassword.generate_reset_token(email)
    reset_url = url_for('app_views.reset_password_token', token=token, _external=True)
    
    # Send the reset link via email
    send_email(
        subject="Password Reset",
        sender=getenv('SMTP_USERNAME'),
        recipients=[email],
        text_body=f"Click the link to reset your password: {reset_url}",
        html_body=f"<p>Click the link to reset your password: <a href='{reset_url}'>{reset_url}</a></p>"
    )
    
    return jsonify({
        "message": "Password reset link sent to email"
    }), 200

# Router to accept token for password reset
@app_views.route('/reset_password/<token>', methods=['GET', 'POST'], strict_slashes=False)
@swag_from('documentation/user/reset_password_with_token.yml')
def reset_password_token(token):
    """
    Handle the password reset link click and update the password
    """
    if request.method == 'GET':
        # Render a form or a simple page to input new password
        return '''
            <form action="" method="post">
                <input type="password" name="new_password" placeholder="New Password">
                <input type="submit" value="Reset Password">
            </form>
        '''
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if not new_password:
            abort(400, description="Missing new password")
        
        email = ResetPassword.verify_reset_token(token)
        if not email:
            abort(400, description="Invalid or expired token")
        
        # Fetch the user from the database
        user = storage.get_user_by_email(email)
        if not user:
            abort(404, description="User not found")
        
        
        # Update the user's password in the database
        user.password = new_password
        storage.save()

        return jsonify({
            "message": "Password has been reset successfully"
        }), 200



# @app_views.route('/reset_password/<token>', methods=['POST'], strict_slashes=False)
# @swag_from('documentation/user/reset_password_with_token.yml')
# def reset_password_token(token):
#     """
#     Handle the password reset link click and update the password
#     """
#     new_password = request.form.get('new_password')
#     if not new_password:
#         abort(400, description="Missing new password")
    
#     email = ResetPassword.verify_reset_token(token)
#     if not email:
#         abort(400, description="Invalid or expired token")
    
#     # Fetch the user from the database
#     user = storage.get_user_by_email(email)
#     if not user:
#         abort(404, description="User not found")
    
#     # Update the user's password in the database
#     user.password = new_password
#     storage.save()

#     return jsonify({
#         "message": "Password has been reset successfully"
#     }), 200
