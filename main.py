from app import app , render_template , socketio

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
    socketio.run(app, debug=True)
        
    


    