from modules import *


load_dotenv()
HOST = os.environ.get('FLASK_HOST')
PORT = os.environ.get('FLASK_PORT')
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

app = Flask(__name__, static_folder='../frontend/build')
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=30)
CORS(app)
socketio = SocketIO(app=app, debug=True, cors_allowed_origins="*", async_mode="eventlet")


# --- WEBSOCKET FUNCTIONS ---

@socketio.on('connect')
def handle_connect():
    print(f"Client connected to server: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected from server: {request.sid}")

@socketio.on('data')
def handle_data(data):
    print(f"Server received: {data}")
    try:
        chat_id, sender_id, sender_username, content, timestamp = data.values()

        sender_id = f"{sender_id}/{request.sid}"
        print(sender_id)
        db.update_chat(session['id'], chat_id, {'option': 'send', 'sender_id': session['id'], 'sender_username': session['username'], 'data': content, 'timestamp': timestamp})

        emit("data", { 'senderId': sender_id, 'senderUserName': sender_username, 'content': content, 'timestamp': timestamp}, broadcast=True)
    except Exception as e:
        log_error(f"Error handling message data, message: {data}", e)

        emit("error", "Something went wrong")

# TODO: handlers for edit/delete


# --- ROUTE FUNCTIONS ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session:
        return jsonify({"error": "User already signed in"}), 400
    if request.method == 'POST':
        data = request.get_json()
        email, username, pw = data.values()

        if db.user_exists(email):
            return jsonify({"error": "A user with that email already exists"})
        res = db.create_user(username, email, pw)

        if res:
            return jsonify({"message": "User created successfully"}), 200
        return jsonify({"error": "Something went wrong! Please try again or contact us"}), 500
    return send_from_directory(app.static_folder, 'index.html'), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return jsonify({"error": "User already signed in"}), 400
    if request.method == 'POST':
        data = request.get_json()
        email, pw = data.values()

        if db.user_exists(email):
            if db.check_pw(email, pw):
                data = db.get_session_data(email)
                session['id'], session['email'], session['username'], session['role'] = data.values()

                return jsonify({"message": "User authenticated successfully"}), 200
        return jsonify({"error": "Email or password incorrect"}), 400
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/userdata', methods=['GET'])
def get_user_data():
    if session:
        if request.method == 'GET':
            data = db.get_user_data_safe(session['id'])

            if data['username']:
                return jsonify({"message": "data retrieved succesfully", "data": data}), 200
            return jsonify({"error": f"Failed to get safe user data for {session['id']} - Error: {data.id}"}), 500
        return jsonify({"error": "Bad method"}), 400
    return jsonify({"error": "No session active"}), 400

@app.route('/chatlist', methods=['GET'])
def get_chat_list():
    if session:
        if request.method == 'GET':
            data = db.get_chat_data(session['id'])

            if data:
                return jsonify({"message": "Chat list retrieved successfully", "data": data}), 200
            return jsonify({"error": f"Failed to retrieve chats for {session['id']}"}), 500
        return jsonify({"error": "Bad method"}), 400
    return jsonify({"error": "No session active"})

@app.route('/chats', methods=['GET', 'POST'])
def get_chats():
    if session:
        if request.method == 'POST':
            id = request.get_data()
            id = id.decode('utf-8').replace("\"", "") # id gets interpreted as bytes

            data = db.get_chat_data(session['id'], id)

            if data:
                return jsonify({"message": "Chats retrieved succesfully", "data": data}), 200
            return jsonify({"error": f"Failed to retrieve chats for {session['id']}"}), 500
        return send_from_directory(app.static_folder, 'index.html')
    return jsonify({"error": "No session active"}), 400


# --- APP SETUP ---

def create_app():
    db.setup()
    # db.populate()
    socketio.run(app=app, host=HOST, port=PORT)


if __name__ == "__main__":
    create_app()