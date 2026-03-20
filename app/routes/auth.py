from flask import Blueprint, request ,jsonify
from app.services.auth_service import register_user , login_user , rotate_refresh_token ,logout_user
from flask_jwt_extended import  jwt_required
from app.services.google_auth_service import google_login


auth=Blueprint("auth",__name__)


@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    response, status = register_user(name, email, password)

    return jsonify(response), status



@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    response, status = login_user(email, password)

    return jsonify(response), status


@auth.route("/refresh",methods=["POST"])
def refresh():
    
    data = request.get_json()
    
    refresh_token=data.get("refresh_token")
    
    if not refresh_token :
        return jsonify({"error": "Refresh Token not found"}), 400
    
    response,status = rotate_refresh_token(refresh_token)
    
    print(refresh_token)
    
    return jsonify(response), status

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    response, status = logout_user()

    return jsonify(response), status



@auth.route("/google_login", methods=["POST"])
def google_auth():

    data = request.get_json()

    token = data.get("token")

    if not token:
        return {"error": "Token required"}, 400

    response, status = google_login(token)

    return jsonify(response), status