from playlist import db
from playlist.models import Song

def existById(id):
        return db.session.query(db.exists().where(Song.id == id)).scalar()

def existsByEmail(email):
        return db.session.query(db.exists().where(Song.email == email)).scalar()

    
