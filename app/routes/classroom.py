from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.classroom_service import create_classroom , regenerate_room_key , join_classroom , leave_classroom , delete_classroom , get_my_classrooms

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
def get_room_key_route(classroom_id):
    
    user_id = get_jwt_identity() 
    response, status = regenerate_room_key(classroom_id,user_id)

    return jsonify(response), status


@classroom_bp.route("/join", methods=["POST"])
@jwt_required()
def join_classroom_route():
    
    user_id = int(get_jwt_identity())
    data = request.get_json()
    response, status = join_classroom(data, user_id)

    return jsonify(response), status


@classroom_bp.route("/leave/<int:classroom_id>",methods=["Delete"])
@jwt_required()
def leave_classroom_route(classroom_id):
    
    user_id = int(get_jwt_identity())
    response, status = leave_classroom(classroom_id, user_id)

    return jsonify(response), status


@classroom_bp.route("/delete/<int:classroom_id>", methods=["DELETE"])
@jwt_required()
def delete_classroom_route(classroom_id):
    user_id = int(get_jwt_identity())

    response, status = delete_classroom(classroom_id, user_id)

    return jsonify(response), status
    
    
@classroom_bp.route("/my_classrooms", methods=["GET"])
@jwt_required()
def my_classrooms():
    user_id = int(get_jwt_identity())

    response, status = get_my_classrooms(user_id)

    return jsonify(response), status
    