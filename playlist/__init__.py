from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf  import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect()
#csrf.init_app(app)
app.config['SECRET_KEY'] = 'c9f2907c6e760b384f32e59aae8cd529'
app.config['SESSION_COOKIE_SECURE'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/db_flask_playlist'
db = SQLAlchemy(app)
app.app_context().push()

from .controllers.UserController import url_user
# from .controllers.PlaylistController import url_playlist
from .controllers.SongController import url_song

app.register_blueprint(url_user, url_prefix="/users")
# app.register_blueprint(url_playlist, url_prefix="/playlists")
app.register_blueprint(url_song,url_prefix="/songs")