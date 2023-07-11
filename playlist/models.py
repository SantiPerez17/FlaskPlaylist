   
import enum
from playlist import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)
    playlists = db.relationship('Playlist', backref='owner', lazy=True)  
    
    def __repr__(self):
        return 'User ("{self.id}","{self.username}","{self.email}")'
    

    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "email":self.email,
            #"playlists": make_playlists(self.id)
        }

def make_playlists(id_user):
        list=[]
        for i in Playlist.query.filter_by(user_id=id_user):
            list.append(i.id)
        return list

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

    id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name=db.Column(db.String(255), nullable=False)
    author=db.Column(db.String(255), nullable=False)
    genre=db.Column(db.Enum(Genre),nullable=False)
    


    def __repr__(self):
        return f"Song('{self.id}','{self.name}', '{self.author}', '{self.genre}')"
    
    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'author':self.author,
            'genre':str(self.genre.name)
        }


class Playlist(db.Model):
    __tablename__="playlists"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    songs = db.relationship('Song', secondary=playlist_song,backref='songs')

    def __repr__(self):
        return f"Playlist('{self.id}','{self.name}','{self.user_id}')"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id":self.user_id,
            "songs": self.songs
        }
