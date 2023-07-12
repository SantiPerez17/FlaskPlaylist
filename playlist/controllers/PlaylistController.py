from flask import Flask, request, jsonify, Blueprint
from playlist.auth import token_required
from playlist import app, db
from playlist.models import Song, Playlist, User
from playlist.services import SongService, UserService, PlaylistService

url_playlist = Blueprint('playlists', __name__)

@url_playlist.route('/', methods=['POST'])
@token_required
def add_playlist(current_user):
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'Invalid Data.'}), 400

    name = json_data.get('name')

    if not name:
        return jsonify({'message': 'Name is required.'}), 400

    user_id = UserService.getIDByEmail(current_user.email)

    existing_playlist = Playlist.query.filter_by(name=name, user_id=user_id).first()

    if existing_playlist:
        return jsonify({'message': 'Playlist already exists.'}), 400

    song_ids = json_data.get('song_ids')

    if song_ids:
        if not all(SongService.existById(song_id) for song_id in song_ids):
            return jsonify({'message': 'One or more songs do not exist.'}), 400

        playlist_result = PlaylistService.create_playlist_with_songs(name, user_id, song_ids)
    else:
        playlist_result = PlaylistService.create_playlist_without_songs(name, user_id)

    if 'error' in playlist_result:
        return jsonify({'message': playlist_result['error']}), 500

    return jsonify({'message': 'Playlist created successfully.', 'playlist': playlist_result['playlist']}), 201


@url_playlist.route("/", methods=["GET"])
def get_playlists():
    playlists = Playlist.query.all()
    serialized_playlists = []

    for playlist in playlists:
        serialized_playlist = playlist.serialize()
        serialized_playlist["songs"] = PlaylistService.serialize_songs(playlist)
        serialized_playlists.append(serialized_playlist)

    return jsonify({'playlists': serialized_playlists}), 200


@url_playlist.route("/myPlaylists", methods=["GET"])
@token_required
def get_my_playlists(current_user):
    user_id = UserService.getIDByEmail(current_user.email)
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    serialized_playlists = []

    for playlist in playlists:
        serialized_playlist = playlist.serialize()
        serialized_playlist["songs"] = PlaylistService.serialize_songs(playlist)
        serialized_playlists.append(serialized_playlist)

    return jsonify({'playlists': serialized_playlists}), 200


@url_playlist.route("/<id>", methods=["GET"])
@token_required
def get_playlist(current_user, id):
    playlist = Playlist.query.filter_by(id=id).first()

    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    elif playlist.user_id != UserService.getIDByEmail(current_user.email):
        return jsonify({'message': 'Access denied.'}), 403

    serialized_playlist = playlist.serialize()
    serialized_playlist["songs"] = PlaylistService.serialize_songs(playlist)

    return jsonify({'playlist': serialized_playlist}), 200


@url_playlist.route("/<id>", methods=["DELETE"])
@token_required
def delete_playlist(current_user, id):
    playlist = Playlist.query.filter_by(id=id).first()

    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    elif playlist.user_id != UserService.getIDByEmail(current_user.email):
        return jsonify({'message': 'Access denied. You are not the owner of this playlist.'}), 403

    try:
        db.session.delete(playlist)
        db.session.commit()
        return jsonify({'message': 'Playlist deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Could not delete playlist.', 'error': str(e)}), 500


@url_playlist.route("/<id>", methods=["PUT"])
@token_required
def update_playlist(current_user, id):
    user_id = UserService.getIDByEmail(current_user.email)
    playlist = Playlist.query.filter_by(id=id).first()

    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    elif playlist.user_id != user_id:
        return jsonify({'message': 'Access denied. You are not the owner of this playlist.'}), 403

    json_data = request.get_json()
    new_name = json_data.get('name')

    if not new_name:
        return jsonify({'message': 'New name is required.'}), 400

    playlists_with_same_name = Playlist.query.filter_by(user_id=user_id, name=new_name).all()
    for p in playlists_with_same_name:
        if p.id != playlist.id:
            return jsonify({'message': 'Playlist with the same name already exists.'}), 400

    playlist.name = new_name

    try:
        db.session.commit()
        return jsonify({'message': 'Playlist updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
    return jsonify({'message': 'Could not update playlist.', 'error': str(e)}), 500

@url_playlist.route("/<id>/songs", methods=["POST"])
@token_required
def add_songs_to_playlist(current_user, id):
    user_id = UserService.getIDByEmail(current_user.email)
    playlist = Playlist.query.filter_by(id=id).first()
    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404
    elif playlist.user_id != user_id:
        return jsonify({'message': 'Access denied. You are not the owner of this playlist.'}), 403

    json_data = request.get_json()
    song_ids = json_data.get('song_ids')

    if not song_ids or not isinstance(song_ids, list):
        return jsonify({'message': 'Invalid song IDs. Please provide a list of song IDs.'}), 400

    existing_song_ids = [song.id for song in playlist.songs]
    new_song_ids = [song_id for song_id in song_ids if song_id not in existing_song_ids]

    songs = Song.query.filter(Song.id.in_(new_song_ids)).all()

    if len(songs) != len(new_song_ids):
        return jsonify({'message': 'Invalid song ID(s).'}), 400

    for song in songs:
        playlist.songs.append(song)

    try:
        db.session.commit()
        return jsonify({'message': 'Songs added to playlist successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Could not add songs to playlist.', 'error': str(e)}), 500

@url_playlist.route('/<playlist_id>/songs/<song_id>', methods=['DELETE'])
@token_required
def delete_song_from_playlist(current_user, playlist_id, song_id):
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    if not playlist:
        return jsonify({'message': 'Playlist not found.'}), 404

    if playlist.user_id != current_user.id:
        return jsonify({'message': 'Access Denied. You are not the owner of this playlist.'}), 403

    song = db.session.query(Song).filter_by(id=song_id).first()

    if not song:
        return jsonify({'message': 'Song not found in the playlist.'}), 404

    try:
        playlist.songs.remove(song)
        db.session.commit()
        return jsonify({'message': 'Song removed from the playlist successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Could not remove song from the playlist.', 'error': str(e)}), 500


