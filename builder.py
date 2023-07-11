from playlist.models import *
from playlist import db

db.create_all()
u1=User(username='rober',email='ju@ju.com',pwd='234')
u2=User(username='roberto',email='ju1@ju.com',pwd='234')

s1=Song(name='alo',author='ese',genre='rock')
s2=Song(name='ali',author='esae',genre='techno')


db.session.add_all([u1,u2,s1,s2])
db.session.commit()

p1=Playlist(name='jo',user_id=u1.id, songs=[s1,s2])
p2=Playlist(name='ja',user_id=u2.id, songs=[s2])
p2.songs.append(s1)
db.session.add_all([p1,p2])

db.session.commit()