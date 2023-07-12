from flask import Flask, request, jsonify, Blueprint
from playlist.auth import token_required
from playlist import app, db
from playlist.models import Song
from playlist.services import SongService,UserService

url_song = Blueprint('songs', __name__)

@url_song.route("/", methods=['POST'])
@token_required
def add_new_song(current_user):
    """
    Endpoint for adding a new song.
    Returns a response with the following structure:
    - Success:
        {
            "message": "Song <song_name> created."
        }
    - Error:
        - If the request data is invalid or missing:
            {
                "message": "Invalid Data."
            }
        - If one or more required fields are missing:
            {
                "message": "Missing required fields."
            }
        - If an error occurs while saving the song:
            {
                "message": "Could not save the information.",
                "error": "<error_message>"
            }
    """
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
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not save the information.', 'error': str(e)}, 500


@url_song.route("/", methods=['GET'])
def list_songs():
    """
    Endpoint for listing all songs.
    Returns a response with the following structure:
    - Success:
        {
            "songs": [
                {
                    "id": <song_id>,
                    "name": <song_name>,
                    "author": <song_author>,
                    "genre": <song_genre>
                },
                ...
            ]
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    try:
        songs = Song.query.all()
        serialized_songs = [song.serialize() for song in songs]
        return {'songs': serialized_songs}, 200
    except Exception as e:
        return {'message': 'Could not retrieve songs.', 'error': str(e)}, 500


@url_song.route("/<id>", methods=['GET'])
def get_song(id):

    """
    Endpoint for retrieving a specific song by ID.
    Returns a response with the following structure:
    - Success:
        {
            "id": <song_id>,
            "name": <song_name>,
            "author": <song_author>,
            "genre": <song_genre>
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """

    song = Song.query.get(id)
    if song:
        return song.serialize(), 200
    else:
        return {'message': 'Song not found.'}, 404

@url_song.route("/<id_song>", methods=['DELETE'])
@token_required
def delete_song(current_user,id_song):

    """
    Endpoint for deleting a song by ID.
    Returns a response with the following structure:
    - Success:
        {
            "message": "Song deleted successfully."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """

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
def update_song(current_user, id_song):

    """
    Endpoint for updating a song by ID.
    Returns a response with the following structure:
    - Success:
        {
            "message": "Song updated successfully."
        }
    - Error:
        {
            "message": "<error_message>"
        }
    """
    
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
        return {'message': 'Song updated successfully.'}, 200
    except:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500

