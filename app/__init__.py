from flask import Flask , render_template , redirect, url_for , Blueprint
from flask_socketio import SocketIO
from  config import Config

config = Config()
socketio = SocketIO() 
blueprint = Blueprint('main', __name__, template_folder='templates')
def create_app():
    app = Flask(__name__)
    from app.routes import blueprint as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app


   

 
