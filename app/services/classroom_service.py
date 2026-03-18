from app.models.classroom import Classroom
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
    