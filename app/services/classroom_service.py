from app.models.classroom import Classroom
from app.models.members import Members
from app.extensions import db
import random
import string

def create_classroom(data, user_id):
    try:
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return {"msg": "Name and description are required"}, 400
        
        room_key=create_room_key()

        classroom = Classroom(
            name=name,
            description=description,
            room_key=room_key,
            created_by=user_id
        )
        db.session.add(classroom)
        db.session.commit()
        new_member = Members(
            classroom_id=classroom.id,
            member_id=user_id,
            is_creator=True
        )
        db.session.add(new_member)
        db.session.commit()

        return {
            "msg": "Classroom created successfully",
            "classroom": classroom.to_dict()
        }, 201

    except Exception as e:
        return {"msg": str(e)}, 500
    

def create_room_key():
    length = 8
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    print(random_string)
    return random_string



def regenerate_room_key(classroom_id,user_id):   
    try:       
        
        classroom = Classroom.query.get(classroom_id)
        
        if classroom.created_by == user_id :
            new_room_key=create_room_key()   
            classroom.room_key = new_room_key
            db.session.commit()
    
            return {
                "msg": "Classroom key updated successfully",
                "classroom": classroom.to_dict()
            }, 200
            
        return{
            "msg": "Only creator can change the room key"
        },400
        
    except Exception as e:
        return{"msg":str(e)},500
    
    
    
def join_classroom(data,user_id):
    
    try:
        room_key = data.get("room_key")
        classroom = Classroom.query.filter_by(room_key=room_key).first()
        
        if not classroom:
            return {"msg": "Invalid room key"}, 404

        
        if classroom.created_by == user_id:
            return {"msg": "You are the creator of this classroom"}, 400

        
        existing = Members.query.filter_by(
            classroom_id=classroom.id,
            member_id=user_id
        ).first()

        if existing:
            return {"msg": "Already joined"}, 400
        
        new_member = Members(
            classroom_id=classroom.id,
            member_id=user_id
        )

        db.session.add(new_member)
        db.session.commit()

        return {
            "msg": "Joined classroom successfully",
            "member": new_member.to_dict()
        }, 200
 
    except Exception as e:
        return{"msg":str(e)},500
    
    
def leave_classroom(classroom_id, user_id):
    try:
        classroom = Classroom.query.get(classroom_id)

        if not classroom:
            return {"msg": "Classroom not found"}, 404


        if classroom.created_by == user_id:
            return {"msg": "Creator cannot leave the classroom"}, 400

        entry = Members.query.filter_by(
            classroom_id=classroom_id,
            member_id=user_id
        ).first()

        if not entry:
            return {"msg": "You are not part of this classroom"}, 400

        db.session.delete(entry)
        db.session.commit()

        return {"msg": "Left classroom successfully"}, 200

    except Exception as e:
        return {"msg": str(e)}, 500
    

    
def delete_classroom(classroom_id, user_id):
    try:
        classroom = Classroom.query.get(classroom_id)

        if not classroom:
            return {"msg": "Classroom not found"}, 404

        if classroom.created_by != user_id:
            return {"msg": "Unauthorized"}, 403

       
        Members.query.filter_by(classroom_id=classroom_id).delete()

        db.session.delete(classroom)
        db.session.commit()

        return {"msg": "Classroom deleted successfully"}, 200

    except Exception as e:
        return {"msg": str(e)}, 500
    
    
def get_my_classrooms(user_id):
    try:
        entries = Members.query.filter_by(member_id=user_id).all()

        created = []
        joined = []

        for entry in entries:
            classroom = Classroom.query.get(entry.classroom_id)

            if entry.is_creator:
                created.append(classroom.to_dict())
            else:
                joined.append(classroom.to_dict())

        return {
            "created_classrooms": created,
            "joined_classrooms": joined
        }, 200

    except Exception as e:
        return {"msg": str(e)}, 500
    