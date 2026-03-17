from google.oauth2 import id_token
from google.auth.transport import requests
from flask import current_app

from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.extensions import db


def google_login(token):

    try:

        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            current_app.config["GOOGLE_CLIENT_ID"]
        )

        email = idinfo["email"]
        name = idinfo["name"]
        google_id = idinfo["sub"]

        user = User.query.filter_by(email=email).first()

        if not user:

            user = User(
                username=name,
                email=email,
                google_id=google_id
            )

            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=user.Uid)
        refresh_token = create_refresh_token(identity=user.Uid)

        token_entry = RefreshToken(
            user_id=user.Uid,
            token=refresh_token
        )

        db.session.add(token_entry)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }, 200

    except ValueError:

        return {"error": "Invalid Google token"}, 401