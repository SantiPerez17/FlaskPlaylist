import datetime
from flask import Blueprint,request,make_response
import jwt
from playlist import db,app
from playlist.models import User 
from werkzeug.security import generate_password_hash, check_password_hash
from playlist.services import UserService
from playlist.auth import token_required



url_user = Blueprint('users',__name__)

@url_user.route("/",methods=['POST'])
def addUser():
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data.'}, 400
    
    if len(json_data)!=3:
        return {'message': 'Invalid Data.'}, 400
    
    if(not UserService.checkEmail(json_data['email'])):
        return {'message': 'The email entered is not valid.'},400
    
    if(UserService.checkExistingEmail(json_data['email'])):
        return {'message': 'The email is already registered.'},400
    
    #Validations
    try:

        username=json_data['username']
        email=json_data['email']
        password=json_data['password']

    except Exception as e:
            return {'message': 'The necessary fields do not exist.'}, 400
    # Save data
    hashed_password = generate_password_hash(password, method='scrypt')
    user = User(username=username, email=email, pwd=hashed_password)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500
    return {'message': 'User '+username+' created.'}, 200

@url_user.route('/login', methods=['GET', 'POST']) # Sensitive
def loginUser():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = User.query.filter_by(email=auth.username).first()
    print(user)
    if user:
        if check_password_hash(user.pwd, auth.password):
            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return {'token': token}
        else:
            return {'message': 'Invalid password.'}
    
    return make_response('Could not verify.',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@url_user.route('/',methods=['GET'])
@token_required
def getUsers(a):
    listUsers=[]
    for i in User.query.all():
        print(i.serialize())
        listUsers.append(i.serialize())
    if listUsers is not None:
        return listUsers, 200
    else:
        return {"error": "Invalid request"}, 400
    
@url_user.route("/<id>",methods=["GET"])
@token_required
def getUser(a,id):
    if UserService.existById(id):
        user=User.query.get(id)
        if (user.id==a.id):
            return {"username": user.username, "email": user.email},200
        else:
            return {'message': 'Is not a current user'},403
    else:
        return {'message': 'User not found.'}, 404


@url_user.route('/<id>',methods=['DELETE'])
@token_required
def deleteUser(a,id):
    if UserService.existById(id):
            user=User.query.get(id)
            if (user.id==a.id):
                db.session.delete(user)
                db.session.commit()  
                return {'message': 'User '+user.username+' deleted successfully.'}              
            else:
                return {'message': 'Is not a current user.'},403
    else:
        return {'message': 'User not found.'}, 404
    

@url_user.route('/<id>',methods=['PUT'])
@token_required
def update_user(a,id):
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data.'}, 400
    if len(json_data)!=2:
        return {'message': 'Invalid Data.'}, 400    
    # Validations
    try:
        username=json_data['username']
        email=json_data['email']
    except Exception as e:
            return {'message': 'The necessary fields do not exist.'}, 400
    # Update data
    if UserService.existById(id):
        user = User.query.get(id)
        print(User.serialize(a))
        print(user)
        if a==user:
            if username != "None":
                user.username = username
            if email != "None":
                    if not (UserService.existByEmail(email) and UserService.checkExistingEmail(email)):
                        user.email = email
                    else:
                        return {'message': 'Email address already in use.'}
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        else:
            return {'message': 'You cannot update the user.'}
    else:
        return {'message': 'User not exist.'}, 500
    return {'message': 'User '+username+' updated.'}, 200