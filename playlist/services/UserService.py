import re
from playlist.models import User
from playlist import db

def checkEmail(email):
    """
    Check if the email is valid.
    Returns True if the email is valid, False otherwise.
    """
    return re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)

def checkExistingEmail(email_user):
    """
    Check if a user with the given email exists in the database.
    Returns True if the user exists, False otherwise.
    """
    return User.query.filter_by(email=email_user).first() is not None

def existById(id):
    """
    Check if a user with the given ID exists in the database.
    Returns True if the user exists, False otherwise.
    """
    return db.session.query(db.exists().where(User.id == id)).scalar()

def existsByEmail(email):
    """
    Check if a user with the given email exists in the database.
    Returns True if the user exists, False otherwise.
    """
    return db.session.query(db.exists().where(User.email == email)).scalar()

def getIDByEmail(email):
    """
    Get the ID of a user with the given email.
    Returns the user ID if found, None otherwise.
    """
    user = db.session.query(User).filter_by(email=email).first()
    return user.id if user else None

def getByEmail(email):
    """
    Get a user by their email.
    Returns the User object if found, None otherwise.
    """
    return db.session.query(User).filter_by(email=email).first()
