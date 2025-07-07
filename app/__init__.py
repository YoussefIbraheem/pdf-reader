from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_socketio import SocketIO
from config import Config
import chromadb
from chromadb.config import Settings

config = Config()
socketio = SocketIO()
blueprint = Blueprint("main", __name__, template_folder="templates")
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=config.CHROMA_DATABASE_URL,
))

def create_app():
    app = Flask(__name__)
    from app.routes import blueprint as home_blueprint

    app.register_blueprint(home_blueprint)

    return app
