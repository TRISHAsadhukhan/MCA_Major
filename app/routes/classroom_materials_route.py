from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.classroom_materials_service import upload_file, get_file_url, delete_file
from app.models.class_materials import File
from app.models.classroom import Classroom
from app.models.members import Members


file_bp = Blueprint("files", __name__)

def is_member(user_id, classroom_id):
    return Members.query.filter_by(
        member_id=user_id,
        classroom_id=classroom_id
    ).first()
    
    
@file_bp.route("/<int:classroom_id>/upload", methods=["POST"])
@jwt_required()
def upload(classroom_id):
    user_id = get_jwt_identity()

    classroom = Classroom.query.get_or_404(classroom_id)

    if classroom.creator_id != user_id:
        return {"error": "Only creator can upload"}, 403

    file = request.files.get("file")

    if not file:
        return {"error": "No file"}, 400

    new_file = upload_file(file, user_id, classroom_id)

    return {
        "message": "Uploaded",
        "file_id": new_file.id
    }, 201
    
    
    
@file_bp.route("/<int:classroom_id>/files", methods=["GET"])
@jwt_required()
def get_files(classroom_id):
    user_id = get_jwt_identity()

    if not is_member(user_id, classroom_id):
        return {"error": "Not a member"}, 403

    files = File.query.filter_by(classroom_id=classroom_id).all()

    return jsonify([
        {
            "id": f.id,
            "filename": f.filename,
            "uploaded_by": f.uploaded_by,
            "created_at": f.created_at
        }
        for f in files
    ])
    
    
    
@file_bp.route("/download/<int:file_id>", methods=["GET"])
@jwt_required()
def download(file_id):
    user_id = get_jwt_identity()

    file = File.query.get_or_404(file_id)

    if not is_member(user_id, file.classroom_id):
        return {"error": "Unauthorized"}, 403

    url = get_file_url(file)

    return {"url": url}



@file_bp.route("/delete/<int:file_id>", methods=["DELETE"])
@jwt_required()
def delete(file_id):
    user_id = get_jwt_identity()

    file = File.query.get_or_404(file_id)
    classroom = Classroom.query.get(file.classroom_id)

    if classroom.creator_id != user_id:
        return {"error": "Only creator can delete"}, 403

    delete_file(file)

    return {"message": "Deleted"}