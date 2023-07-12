from playlist import db
from playlist.models import Song

def existById(id):
    """
    Check if a song with the given ID exists in the database.
    Returns True if the song exists, False otherwise.
    """
    return db.session.query(db.exists().where(Song.id == id)).scalar()

def existsByEmail(email):
    """
    Check if a song with the given email exists in the database.
    Returns True if the song exists, False otherwise.
    """
    return db.session.query(db.exists().where(Song.email == email)).scalar()


    
