from flask import Flask, request, jsonify, Blueprint
from playlist.auth import token_required
from playlist import app, db
from playlist.models import Song
from playlist.services import SongService,UserService

url_song = Blueprint('songs', __name__)

@url_song.route("/", methods=['POST'])
@token_required
def add_new_song(current_user):
    json_data = request.get_json()

    if not json_data or len(json_data) != 3:
        return {'message': 'Invalid Data.'}, 400

    name = json_data.get('name')
    author = json_data.get('author')
    genre = json_data.get('genre')

    if not all([name, author, genre]):
        return {'message': 'Missing required fields.'}, 400

    song = Song(name=name, author=author, genre=genre)
    db.session.add(song)

    try:
        db.session.commit()
        return {'message': 'Song {} created.'.format(song.name)}, 200
    except:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500

@url_song.route("/", methods=['GET'])
def list_songs():
    songs = Song.query.all()
    serialized_songs = [song.serialize() for song in songs]
    return {'songs': serialized_songs}, 200

@url_song.route("/<id>", methods=['GET'])
def get_song(id):
    if not SongService.existById(id):
        return {'message': 'Song not found.'}, 404

    song = Song.query.get(id)
    if song:
        return song.serialize(), 200
    else:
        return {'message': 'Song not found.'}, 404

@url_song.route("/<id_song>", methods=['DELETE'])
@token_required
def delete_song(current_user,id_song):
    song = Song.query.get(id_song)

    if not song:
        return {'message': 'Song not found.'}, 404

    if not UserService.existsByEmail(current_user.email):
        return {'message': 'Unauthorized. Token email does not match user email.'}, 401


    db.session.delete(song)

    try:
        db.session.commit()
        return {'message': 'Song deleted successfully.'}, 200
    except:
        db.session.rollback()
        return {'message': 'Could not delete song.'}, 500

@url_song.route("/<id_song>", methods=['PUT'])
@token_required
def update_song(current_user,id_song):
    if not UserService.existsByEmail(current_user.email):
        return {'message': 'Unauthorized. Token email does not match user email.'}, 401


    json_data = request.get_json()

    if not json_data or len(json_data) != 3:
        return {'message': 'Invalid Data.'}, 400

    name = json_data.get('name')
    author = json_data.get('author')
    genre = json_data.get('genre')

    if not any([name, author, genre]):
        return {'message': 'No fields to update.'}, 400

    song = Song.query.get(id_song)

    if not song:
        return {'message': 'Song not found.'}, 404

    song.name = name if name else song.name
    song.author = author if author else song.author
    song.genre = genre if genre else song.genre

    try:
        db.session.commit()
        return {'message': 'Song {} updated.'.format(song.name)}, 200
    except:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500
