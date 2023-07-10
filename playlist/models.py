   
import enum
from playlist import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)
    playlists = db.relationship('Playlist', backref='owner', lazy=True)  
    
    def __repr__(self):
        return f'<User ("{self.id}","{self.username}","{self.email}")>'

class Genre(enum.Enum):
    ROCK="rock"
    TECHNO="techno"
    POP="pop"
    JAZZ="jazz"
    FOLK="folk"
    CLASSICAL="classical"


playlist_song = db.Table("playlist_song",
                 db.Column('playlist_id',db.Integer(),db.ForeignKey('playlists.id'))
                 ,
                 db.Column('song_id',db.Integer(),db.ForeignKey('songs.id'))
                 )

class Song(db.Model):
    __tablename__= "songs"

    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    author=db.Column(db.String(255), nullable=False)
    genre=db.Column(db.Enum(Genre))
    


    def __repr__(self):
        return f"<Song('{self.id}','{self.name}', '{self.author}', '{self.genre}')>"
    



class Playlist(db.Model):
    __tablename__="playlists"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #user = db.relationship("User", lazy="joined", innerjoin=True)
    songs = db.relationship('Song', secondary=playlist_song,backref='songs')


