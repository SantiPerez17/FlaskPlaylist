import datetime
from flask import Blueprint,request,make_response
import jwt
from playlist import db,app
from playlist.models import User 
from werkzeug.security import generate_password_hash, check_password_hash
from playlist.services import UserService
from playlist.auth import token_required



url_user = Blueprint('users',__name__)

@url_user.route("/", methods=['POST'])
def add_user():

    """
    Endpoint for adding a new user.
    Requires the following fields in the request JSON data:
    - email: Email address of the user.
    - username: Username of the user.
    - password: Password of the user.
    Returns a response with the following structure:
    - Success:
        {
            "message": "User <username> created."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    
    json_data = request.get_json()

    if not json_data:
        return {'message': 'Invalid Data.'}, 400

    if len(json_data) != 3:
        return {'message': 'Invalid Data.'}, 400

    email = json_data.get('email')
    username = json_data.get('username')
    password = json_data.get('password')

    if not email or not username or not password:
        return {'message': 'Missing required fields.'}, 400

    if not UserService.checkEmail(email):
        return {'message': 'The email entered is not valid.'}, 400

    if UserService.checkExistingEmail(email):
        return {'message': 'The email is already registered.'}, 400

    # Save data
    hashed_password = generate_password_hash(password, method='scrypt')
    user = User(username=username, email=email, pwd=hashed_password)
    db.session.add(user)

    try:
        db.session.commit()
        return {'message': 'User {} created.'.format(username)}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500


@url_user.route('/login', methods=['POST'])
def login_user():

    """
    Endpoint for user login.
    Returns an authentication token upon successful login.
    Returns an error message if login fails.
    Returns a response with the following structure:
    - Success:
        {
            "token": "<authentication_token>"
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return {'message': 'Invalid Data.'}, 400

    user = User.query.filter_by(email=auth.username).first()

    if user:
        if check_password_hash(user.pwd, auth.password):
            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3)}, app.config['SECRET_KEY'])
            return {'token': token}, 200
        else:
            return {'message': 'Invalid password.'}, 401

    return {'message': 'Could not verify.'}, 401


@url_user.route('/', methods=['GET'])
@token_required
def get_users(current_user):

    """
    Endpoint for retrieving all users.
    Requires authentication token in the request headers.
    Returns a response with the following structure:
    - Success:
        {
            "users": [
                {
                    "username": "<username_1>",
                    "email": "<email_1>",
                    "id": "<id_1>"
                },
                {
                    "username": "<username_2>",
                    "email": "<email_2>",
                    "id": "<id_2>"
                },
                ...
            ]
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    try:
        users = User.query.all()
        serialized_users = [user.serialize() for user in users]
        return {'users': serialized_users}, 200
    except Exception as e:
        return {'message': 'Could not retrieve users.', 'error': str(e)}, 500

    
@url_user.route("/<id>", methods=["GET"])
@token_required
def get_user(current_user, id):

    """
    Endpoint for retrieving user information.
    Requires authentication token in the request headers.
    Accepts the user ID as a path parameter.
    Returns a response with the following structure:
    - Success:
        {
            "username": "<username>",
            "email": "<email>"
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """

    if not UserService.existById(id):
        return {'message': 'User not found.'}, 404

    user = User.query.get(id)
    if user.id != current_user.id:
        return {'message': 'Access denied. You are not the owner of this user.'}, 403

    return {'username': user.username, 'email': user.email}, 200



@url_user.route('/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):

    """
    Endpoint for deleting a user.
    Requires authentication token in the request headers.
    Accepts the user ID as a path parameter.
    Returns a response with the following structure:
    - Success:
        {
            "message": "User <username> deleted successfully."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """

    if not UserService.existById(id):
        return {'message': 'User not found.'}, 404

    user = User.query.get(id)
    if user.id != current_user.id:
        return {'message': 'Access denied. You are not this user.'}, 403

    try:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User {} deleted successfully.'.format(user.username)}
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not delete user.', 'error': str(e)}, 500

    

@url_user.route('/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    """
    Endpoint for updating user information.
    Requires authentication token in the request headers.
    Expects a JSON object in the request body with optional fields:
    {
        "username": "<new_username>",
        "email": "<new_email>"
    }
    Returns a response with the following structure:
    - Success:
        {
            "message": "User <username> updated."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data.'}, 400
    
    # Validations
    try:
        username = json_data.get('username')
        email = json_data.get('email')
    except Exception as e:
        return {'message': 'The necessary fields do not exist.'}, 400
    
    # Update data
    if not UserService.existById(id):
        return {'message': 'User not found.'}, 404
    
    user = User.query.get(id)
    if current_user != user:
        return {'message': 'Access denied. You are not the owner of this user.'}, 403
    
    user.username = username if username is not None else user.username
    
    if email is not None:
        if not UserService.existByEmail(email) or user.email == email:
            user.email = email
        else:
            return {'message': 'Email address already in use.'}, 400
    
    try:
        db.session.commit()
        return {'message': 'User {} updated.'.format(user.username)}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not update user.', 'error': str(e)}, 500

@url_user.route('/change_password', methods=['PUT'])
@token_required
def change_password(current_user):
    """
    Endpoint for changing user's password.
    Requires authentication token in the request headers.
    Expects a JSON object in the request body with the following format:
    {
        "current_password": "<current_password>",
        "new_password": "<new_password>"
    }
    Returns a response with the following structure:
    - Success:
        {
            "message": "Password changed successfully."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data. No JSON data provided.'}, 400
    
    # Validations
    try:
        current_password = json_data.get('current_password')
        new_password = json_data.get('new_password')
    except Exception as e:
        return {'message': 'The necessary fields do not exist.'}, 400
    
    if not len(json_data) == 2:
        return {'message': 'Invalid Data. The JSON file is incorrect.'},400


    # Check if current password is correct
    user=User.query.get(current_user.id)
    if not check_password_hash(str(user.pwd), str(current_password)):
        return {'message': 'Invalid current password.'}, 400
    
    # Update password
    
    user.pwd = generate_password_hash(str(new_password), method='scrypt')
    
    try:
        db.session.commit()
        return {'message': 'Password changed successfully.'}, 200
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not change password.', 'error': str(e)}, 500
