from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_socketio import SocketIO
from config import Config
import chromadb
from chromadb.config import Settings
from flask_sqlalchemy import SQLAlchemy

config = Config()
socketio = SocketIO()
blueprint = Blueprint("main", __name__, template_folder="templates")
chroma_client = chromadb.PersistentClient(path=config.CHROMA_DATABASE_URI)
db = SQLAlchemy()

print(config.SQLALCHEMY_DATABASE_URI)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    from app.routes import blueprint as home_blueprint

    app.register_blueprint(home_blueprint)

    return app
