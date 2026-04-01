
from app.utils.supabase_client import supabase, BUCKET
from app.models.class_materials import File
from app.extensions import db
import uuid

def upload_file(file, user_id, classroom_id):
    unique_name = f"{classroom_id}/{uuid.uuid4()}_{file.filename}"

    # upload to supabase
    supabase.storage.from_(BUCKET).upload(
        unique_name,
        file.read()
    )

    new_file = File(
        filename=file.filename,
        filepath=unique_name,
        classroom_id=classroom_id,
        uploaded_by=user_id
    )

    db.session.add(new_file)
    db.session.commit()

    return new_file



def get_file_url(file):
    return supabase.storage.from_(BUCKET).create_signed_url(
        file.filepath,
        60
    )
    
    
    
def delete_file(file):
    supabase.storage.from_(BUCKET).remove([file.filepath])

    db.session.delete(file)
    db.session.commit()