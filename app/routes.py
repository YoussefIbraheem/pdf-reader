from app import render_template , Blueprint , blueprint


@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/chat')
def chat():
    return render_template('chat.html')