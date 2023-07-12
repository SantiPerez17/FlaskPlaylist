import re
from playlist.models import User
from playlist import db

def checkEmail(email):
    return re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email)

def checkExistingEmail(email_user):
    return User.query.filter_by(email=email_user).first() != None

def existById(id):
        return db.session.query(db.exists().where(User.id == id)).scalar()

def existsByEmail(email):
     return db.session.query(db.exists().where(User.email == email)).scalar()

def getIDByEmail(email):
    user=db.session.query(User).filter_by(email=email).first()
    return user.id

def getByEmail(email):
     return db.session.query(User).filter_by(email=email).first()