from flask import Flask , render_template , redirect, url_for
from flask_socketio import SocketIO


socketio = SocketIO() 

def create_app():
    app = Flask(__name__)
 
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
       
   

 
