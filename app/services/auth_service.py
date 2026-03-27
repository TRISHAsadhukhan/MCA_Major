from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.token_blacklist import TokenBlacklist
from app.extensions import db , bcrypt

from flask_jwt_extended import create_access_token , create_refresh_token , decode_token , get_jwt



# SIGNUP
def register_user(name, email, password):

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "Email already exists"}, 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully"
    }, 201



# LOGIN

def login_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid email or password"}, 401

    if not bcrypt.check_password_hash(user.password, password):
        return {"error": "Invalid email or password"}, 401
    
    access_token = create_access_token(identity=str(user.Uid))
    refresh_token = create_refresh_token(identity=str(user.Uid))

    token_entry = RefreshToken(
        user_id=user.Uid,
        token=refresh_token
    )
    
    db.session.add(token_entry)
    db.session.commit()

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }, 200
  

  
# Refresh_token rotate

def rotate_refresh_token(old_token):

    decoded = decode_token(old_token)

    user_id = decoded["sub"]

    token_entry = RefreshToken.query.filter_by(token=old_token).first()

    if not token_entry or token_entry.is_revoked:
        return {"error": "Invalid refresh token"}, 401

    token_entry.is_revoked = True

    new_access_token = create_access_token(identity=str(user_id))
    new_refresh_token = create_refresh_token(identity=str(user_id))

    new_token_entry = RefreshToken(
        user_id=user_id,
        token=new_refresh_token
    )

    db.session.add(new_token_entry)
    db.session.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }, 200
    
    
def logout_user():

    jwt_data = get_jwt()
 
    jti = jwt_data["jti"]
    user_id = jwt_data["sub"]

    # 1️⃣ blacklist access token
    blacklisted = TokenBlacklist(jti=jti)
    db.session.add(blacklisted)

    # 2️⃣ revoke all refresh tokens of user
    RefreshToken.query.filter_by(user_id=user_id, is_revoked=False)\
        .update({"is_revoked": True})

    db.session.commit()

    return {"message": "Logout successful"}, 200