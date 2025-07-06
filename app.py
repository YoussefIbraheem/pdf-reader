from app import app, socketio



if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
    socketio.run(app, debug=True)
        
    


    