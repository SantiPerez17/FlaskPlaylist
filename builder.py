import random
from playlist import db, app
from playlist.models import User, Song, Playlist
from werkzeug.security import generate_password_hash
from enum import Enum

# Definir enum de géneros de canciones
class Genre(Enum):
    ROCK = 'rock'
    TECHNO = 'techno'
    POP = 'pop'
    JAZZ = 'jazz'
    FOLK = 'folk'
    CLASSICAL = 'classical'

# Lista de nombres de canciones famosas por género
rock_songs = [
    ('Bohemian Rhapsody', 'Queen'),
    ('Stairway to Heaven', 'Led Zeppelin'),
    ('Hotel California', 'Eagles'),
    ('Smells Like Teen Spirit', 'Nirvana'),
    ('Sweet Child o\' Mine', 'Guns N\' Roses')
]
techno_songs = [
    ('Around the World', 'Daft Punk'),
    ('Sandstorm', 'Darude'),
    ('One More Time', 'Daft Punk'),
    ('Insomnia', 'Faithless'),
    ('Levels', 'Avicii')
]
pop_songs = [
    ('Billie Jean', 'Michael Jackson'),
    ('Shape of You', 'Ed Sheeran'),
    ('Like a Prayer', 'Madonna'),
    ('Uptown Funk', 'Mark Ronson ft. Bruno Mars'),
    ('Hello', 'Adele')
]
jazz_songs = [
    ('Summertime', 'Ella Fitzgerald'),
    ('Fly Me to the Moon', 'Frank Sinatra'),
    ('Take Five', 'Dave Brubeck Quartet'),
    ('All Blues', 'Miles Davis'),
    ('So What', 'Miles Davis')
]
folk_songs = [
    ('Blowin\' in the Wind', 'Bob Dylan'),
    ('The Times They Are a-Changin\'', 'Bob Dylan'),
    ('Hallelujah', 'Leonard Cohen'),
    ('Mr. Tambourine Man', 'Bob Dylan'),
    ('Imagine', 'John Lennon')
]
classical_songs = [
    ('Für Elise', 'Ludwig van Beethoven'),
    ('Moonlight Sonata', 'Ludwig van Beethoven'),
    ('Canon in D', 'Johann Pachelbel'),
    ('The Four Seasons', 'Antonio Vivaldi'),
    ('Symphony No. 9', 'Ludwig van Beethoven')
]

def create_users():
    users = []
    for i in range(1, 16):
        email = f'user{i}@playlist.com'
        hashed_password = generate_password_hash('1234', method='scrypt')
        user = User(username=f'User {i}', email=email, pwd=hashed_password)
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

def create_songs():
    songs = []
    for _ in range(150):
        genre = random.choice(list(Genre))
        if genre == Genre.ROCK:
            name, author = random.choice(rock_songs)
        elif genre == Genre.TECHNO:
            name, author = random.choice(techno_songs)
        elif genre == Genre.POP:
            name, author = random.choice(pop_songs)
        elif genre == Genre.JAZZ:
            name, author = random.choice(jazz_songs)
        elif genre == Genre.FOLK:
            name, author = random.choice(folk_songs)
        else:
            name, author = random.choice(classical_songs)

        song = Song(name=name, author=author, genre=genre.name)
        songs.append(song)

    db.session.add_all(songs)
    db.session.commit()

def create_playlists():
    users = User.query.all()
    playlists = []
    for user in users:
        num_playlists = random.randint(5, 20)
        for _ in range(num_playlists):
            name = f'Playlist {random.randint(1, 1000)}'
            genre = random.choice(list(Genre))
            num_songs = random.randint(10, 40)
            song_ids = random.sample(range(1, 151), num_songs)
            playlist = Playlist(name=name, user_id=user.id)
            playlist.songs.extend(Song.query.filter(Song.id.in_(song_ids)).all())
            playlists.append(playlist)

    db.session.add_all(playlists)
    db.session.commit()

def build_database():
    with app.app_context():
        db.create_all()
        create_users()
        create_songs()
        create_playlists()

if __name__ == '__main__':
    build_database()
