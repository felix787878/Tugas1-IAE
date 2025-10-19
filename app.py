import os
from datetime import datetime, timedelta
from functools import wraps
import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

server = Flask(__name__)

server.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
SERVER_PORT = os.getenv("PORT", 5000)

db_users = {
    "twin@towers.com": {
        "password": "takbir",
        "profile": {"name": "osama", "email": "osama@plane.com"},
    }
}

db_items = [
    {"id": 1, "nama": "lemari", "harga": 1000},
    {"id": 2, "nama": "meja", "harga": 2000},
    {"id": 3, "nama": "pesawat", "harga": 3000},
]

def check_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Header Otorisasi tidak valid atau tidak ada"}), 401

        token_string = auth_header.split(" ")[1]

        try:
            claims = jwt.decode(
                token_string, server.config["JWT_SECRET"], algorithms=["HS256"]
            )
            request.user_claims = claims
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

@server.route("/auth/login", methods=["POST"])
def handle_login():
    auth_data = request.get_json()
    if not auth_data or not auth_data.get("email") or not auth_data.get("password"):
        return jsonify({"error": "Email dan password dibutuhkan"}), 400

    email = auth_data["email"]
    password = auth_data["password"]

    account = db_users.get(email)
    if not account or account["password"] != password:
        return jsonify({"error": "Email atau password salah"}), 401

    token_payload = {
        "sub": email,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }

    access_token = jwt.encode(
        token_payload, server.config["JWT_SECRET"], algorithm="HS256"
    )

    print(f"Login berhasil untuk: {email}")
    return jsonify({"access_token": access_token})

@server.route("/items", methods=["GET"])
def get_all_items():
    return jsonify({"items": db_items})

@server.route("/profile", methods=["PUT"])
@check_token
def modify_profile():
    user_identifier = request.user_claims["sub"]

    user_account = db_users.get(user_identifier)
    if not user_account:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404

    new_data = request.get_json()
    if not new_data or ("name" not in new_data and "email" not in new_data):
        return jsonify({"error": "Body permintaan harus berisi 'name' atau 'email'"}), 400

    if "name" in new_data:
        user_account["profile"]["name"] = new_data["name"]
    if "email" in new_data:
        user_account["profile"]["email"] = new_data["email"]

    print(f"Profil untuk {user_identifier} berhasil diperbarui.")
    return jsonify(
        {"message": "Profil berhasil diperbarui", "profile": user_account["profile"]}
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(SERVER_PORT), debug=True)