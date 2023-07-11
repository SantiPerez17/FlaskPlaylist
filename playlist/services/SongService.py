from playlist import db
from playlist.models import Song

def existById(id):
        return db.session.query(Song.query.filter(Song.id == id).exists())

    
