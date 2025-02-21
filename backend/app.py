from modules import *

app = Flask(__name__, static_folder='../frontend/build')
app.secret_key = 'my_secret'
app.permanent_session_lifetime = timedelta(minutes=30)
CORS(app)
socketio = SocketIO(app=app, debug=True, cors_allowed_origins="*", async_mode="eventlet")


# --- WEBSOCKET FUNCTIONS ---

@socketio.on('connect')
def handle_connect():
    print("Client connected to server")
    socketio.emit("message", "Client connected to server")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected from server")
    socketio.emit("message", "Client disconnected from server")


# --- FLASK FUNCTIONS ---

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

if __name__ == "__main__":

    socketio.run(app=app, port=5000)
    db.setup()