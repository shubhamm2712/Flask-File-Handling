from flask import request
from datetime import datetime, timedelta
import jwt

from auth_db import tokenNotBlacklist
from config import config
from database import UserDB, db
from exceptions import CustomExceptions

def generate_token(user: UserDB):
    exp = datetime.now() + timedelta(minutes=60)
    payload = {
        "user": user.toToken(),
        "exp": exp.timestamp()
    }
    token = jwt.encode(payload, config.secret_key, algorithm="HS256")
    return token

def verify_token():
    if "Authorization" not in request.headers:
        raise CustomExceptions("Authorization missing", 401)
    bearer_token = request.headers["Authorization"]
    if not bearer_token.startswith("Bearer "):
        raise CustomExceptions("Invalid Bearer token", 401)
    token = bearer_token.split(" ")[1]
    try:
        payload = jwt.decode(token, config.secret_key, algorithms="HS256")
        if "user" not in payload:
            raise CustomExceptions("Invalid token passed", 401)
        if not tokenNotBlacklist(token):
            raise CustomExceptions("Invalid token", 401)
        user = UserDB(**payload["user"])
        return user, token
    except CustomExceptions as e:
        raise e
    except KeyError as e:
        raise CustomExceptions("Invalid token, key error: "+str(e), 401)
    except Exception as e:
        raise CustomExceptions("Exception in token verification "+str(e), 401)