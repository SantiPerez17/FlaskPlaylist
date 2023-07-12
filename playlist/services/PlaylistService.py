from playlist.models import Playlist, Song
from playlist import db

def existById(id):
    return db.session.query(db.exists().where(Playlist.id == id)).scalar()

def existsByName(name):
    return db.session.query(db.exists().where(Playlist.name == name)).scalar()

def getPlaylists():
    return Playlist.query.all()

def checkExistPlaylist(name,user_id):
    return db.session.query(Playlist).filter_by(name=name, user_id=user_id).first()


def getPlaylistsByUserId(user_id):
    return db.session.query(Playlist).filter(Playlist.user_id == user_id).all()

def getPlaylist(id):
    return Playlist.query.get(id)


def serialize_songs(playlist):
    serialized_songs = []
    for song in playlist.songs:
        serialized_songs.append(song.serialize())
    return serialized_songs


@staticmethod
def create_playlist_without_songs(name, user_id):
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
