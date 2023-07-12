from playlist.models import Playlist, Song
from playlist import db

def existById(id):
    """
    Check if a playlist with the given ID exists in the database.
    Returns True if the playlist exists, False otherwise.
    """
    return db.session.query(db.exists().where(Playlist.id == id)).scalar()

def existsByName(name):
    """
    Check if a playlist with the given name exists in the database.
    Returns True if the playlist exists, False otherwise.
    """
    return db.session.query(db.exists().where(Playlist.name == name)).scalar()

def getPlaylists():
    """
    Retrieve all playlists from the database.
    Returns a list of Playlist objects.
    """
    return Playlist.query.all()

def checkExistPlaylist(name, user_id):
    """
    Check if a playlist with the given name and user ID exists in the database.
    Returns the playlist object if it exists, None otherwise.
    """
    return db.session.query(Playlist).filter_by(name=name, user_id=user_id).first()

def getPlaylistsByUserId(user_id):
    """
    Retrieve all playlists belonging to the user with the given ID.
    Returns a list of Playlist objects.
    """
    return db.session.query(Playlist).filter(Playlist.user_id == user_id).all()

def getPlaylist(id):
    """
    Retrieve a playlist by its ID.
    Returns the Playlist object if found, None otherwise.
    """
    return Playlist.query.get(id)

def serialize_songs(playlist):
    """
    Serialize the songs of a playlist into a list of dictionaries.
    Returns a list of serialized song dictionaries.
    """
    serialized_songs = []
    for song in playlist.songs:
        serialized_songs.append(song.serialize())
    return serialized_songs

@staticmethod
def create_playlist_without_songs(name, user_id):
    """
    Create a new playlist without any songs.
    Returns a dictionary with the serialized playlist if successful.
    If there is an error, returns a dictionary with an error message.
    """
    try:
        playlist = Playlist(name=name, user_id=user_id, songs=[])
        db.session.add(playlist)
        db.session.commit()
        return {'playlist': playlist.serialize()}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Could not create playlist.', 'details': str(e)}

@staticmethod
def create_playlist_with_songs(name, user_id, song_ids):
    """
    Create a new playlist with the specified songs.
    Returns a dictionary with the serialized playlist if successful.
    If there is an error, returns a dictionary with an error message.
    """
    try:
        songs = Song.query.filter(Song.id.in_(song_ids)).all()
        existing_song_ids = [song.id for song in songs]
        non_existing_song_ids = [song_id for song_id in song_ids if song_id not in existing_song_ids]

        if non_existing_song_ids:
            return {'error': f'Song(s) with ID(s) {non_existing_song_ids} do not exist.'}

        playlist = Playlist(name=name, user_id=user_id)
        playlist.songs = songs

        db.session.add(playlist)
        db.session.commit()

        return {'playlist': playlist.serialize()}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Could not create playlist.', 'details': str(e)}

