   
import enum
from playlist import db
from flask import UserMixin

from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<User ("{self.id}","{self.username}","{self.email}")>'

class Genre(enum.Enum):
    ROCK="rock"
    TECHNO="techno"
    POP="pop"
    JAZZ="jazz"
    FOLK="folk"
    CLASSICAL="classical"


class Song(db.Model):
    __tablename__= "songs"

    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    author=db.Column(db.String(255), nullable=False)
    genre=db.Column(db.Enum(Genre))

    def __repr__(self):
        return f"<Song('{self.id}','{self.name}', '{self.author}', '{self.genre.name}')>"
    

playlist_song = ("playlist_song",
                 db.Column('playlist_id',db.Integer(),db.ForeignKey('playlist.id'))
                 ,
                 db.Column('song_id',db.Integer(),db.ForeignKey('song.id'))
                 )

class Playlist(db.Model):
    __tablename__="playlists"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_song,backref='songs')


