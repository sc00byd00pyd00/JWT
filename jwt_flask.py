from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Dummy user database
users = {
    "admin": {"password": "password123", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username in users and users[username]["password"] == password:
        user_identity = {"username": username, "role": users[username]["role"]}
        access_token = create_access_token(identity=user_identity)
        refresh_token = create_refresh_token(identity=user_identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify(access_token=new_access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    return jsonify({"msg": "Welcome Admin"}), 200

@app.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    return jsonify(users=list(users.keys())), 200

@app.route('/add_user', methods=['POST'])
@jwt_required()
def add_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")
    
    if username in users:
        return jsonify({"msg": "User already exists"}), 400
    
    users[username] = {"password": password, "role": role}
    return jsonify({"msg": "User added successfully"}), 201

@app.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    
    data = request.get_json()
    username = data.get("username")
    
    if username not in users:
        return jsonify({"msg": "User not found"}), 404
    
    del users[username]
    return jsonify({"msg": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
