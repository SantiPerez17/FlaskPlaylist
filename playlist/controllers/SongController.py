from flask import Flask,request,jsonify,make_response,Blueprint
from playlist import app, db
from playlist.models import *
import json 



url_song = Blueprint('song', __name__)

@url_song.route("/",methods=['POST'])
def addSong():
	data = request.get_json()
	song=Song(name=data['name'],author=data['author'],genre=data['genre'])
	db.session.add(song)
	db.session.commit()
	return jsonify({'message': 'ok'}),200

@url_song.route("/",methods=['GET'])
def listSongs():
    a={}
    a['songs']=[]
    for i in Song.query.all():
          a['songs'].append(i.serialize())
          print(i.serialize())
    return a,200


@url_song.route("/<id>",methods=['GET'])
def getSong(id):
      return Song.query.get(id).serialize(),200

@url_song.route("/<id_song>",methods=['DELETE'])
def deleteSong(id_song):
    song=Song.query.filter_by(id=id_song).first()
    print(song)
    db.session.delete(song)
    db.session.commit()
    return 'ok',200

@url_song.route("/<id_song>",methods=['PUT'])
def updateSong(id_song):
    song=Song.query.filter_by(id=id_song).first()
    print(song)
    #song = Song.query.get(id_song)
    #print(song)
    name=request.json['name']
    author=request.json['author']
    genre=request.json['genre']
    
    if name != "None":
        song.name=name
    if author != "None":
        song.author=author
    if genre != "None":
        song.genre=genre

    db.session.commit()  
        
    return jsonify({'message':'Song updated.'})
  



