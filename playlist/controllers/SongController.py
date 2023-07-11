from flask import Flask,request,jsonify,make_response,Blueprint
from playlist import app, db
from playlist.models import *
from playlist.services import SongService
#from playlist.services.SongService import *
import json 



url_song = Blueprint('song', __name__)


@url_song.route("/",methods=['POST'])
def addnewSong():
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data.'}, 400
    if len(json_data)!=3:
        return {'message': 'Invalid Data.'}, 400    
    # Validations
    try:
        name=json_data['name']
        author=json_data['author']
        genre=json_data['genre']
    except Exception as e:
            return {'message': 'The necessary fields do not exist.'}, 400
    # Save data
    song = Song(name=name, author=author, genre=genre)
    db.session.add(song)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'message': 'Could not save the information.'}, 500
    return {'message': 'Song '+name+' created.'}, 200

@url_song.route("/",methods=['GET'])
def listSongs():
    listSongs={}
    listSongs=[]
    for i in Song.query.all():
        listSongs.append(i.serialize())
    if listSongs is not None:
        return listSongs,200
    else:
        return jsonify({"error": "Invalid request"}), 400


@url_song.route("/<id>",methods=['GET'])
def getSong(id):
    if SongService.existById(id):
        song = Song.query.get(id)
        #print(song)
        return Song.serialize(song)
    else:
        return {'message': 'Song not found.'}, 404

@url_song.route("/<id_song>",methods=['DELETE'])
def deleteSong(id_song):
    song = Song.query.get(id_song)
    if song:
        db.session.delete(song)
        db.session.commit()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Could not delete song.'}, 500
    else:
        return {'message': 'Song not found.'}, 400
    return {'message': 'ok'}, 200

@url_song.route("/<id_song>",methods=['PUT'])
def updateSong(id_song):
    json_data = request.get_json()
    if not json_data:
        return {'message': 'Invalid Data.'}, 400
    if len(json_data)!=3:
        return {'message': 'Invalid Data.'}, 400    
    # Validations
    try:
        name=json_data['name']
        author=json_data['author']
        genre=json_data['genre']
    except Exception as e:
            return {'message': 'The necessary fields do not exist.'}, 400
    # Save data
    if SongService.existById(id):
        song = Song.query.get(id_song)
        if name != "None":
            song.name=name
        if author != "None":
            song.author=author
        if genre != "None":
            song.genre=genre
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    else:
        return {'message': 'Could not save the information.'}, 500
    return {'message': 'Song '+name+' updated.'}, 200
  



