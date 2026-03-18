from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.classroom_service import create_classroom , regenerate_room_key

classroom_bp = Blueprint("classroom", __name__)

@classroom_bp.route("/create", methods=["POST"])
@jwt_required() 
def create_classroom_route():
    user_id = get_jwt_identity()  

    data = request.get_json()

    response, status = create_classroom(data, user_id)

    return jsonify(response), status


@classroom_bp.route("/get_room_key/<int:classroom_id>",methods=["PUT"])
@jwt_required()
def get_room_key(classroom_id):
    
    user_id = get_jwt_identity() 
    response, status = regenerate_room_key(classroom_id,user_id)

    return jsonify(response), status