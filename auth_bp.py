from flask import Blueprint, request

from auth import verify_token
from database import UserDB, db
import db_ops
from exceptions import CustomExceptions

bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"].strip()
        username = username or None
        password = data["password"].strip()
        password = password or None
        if username is None or password is None:
            raise CustomExceptions("Username or Password is missing", 400)
        access_token = db_ops.login(username, password)
        return access_token
    except CustomExceptions as e:
        return e.response()
    except KeyError as e:
        return {"message": "Exception: Missing "+str(e)}, 400
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 400

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data["username"].strip()
        username = username or None
        password = data["password"].strip()
        password = password or None
        name = data["name"].strip()
        name = name or name
        description = data.get("description", "").strip()
        if username is None or password is None or name is None:
            raise CustomExceptions("Username, Password or name is missing", 400)
        user = UserDB(username, password, name, description)
        db_ops.register(user)
        return {"message": "Successfully registered"}
    except CustomExceptions as e:
        return e.response()
    except KeyError as e:
        return {"message": "Exception: Missing "+str(e)}, 400
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 400

@bp.route("/logout", methods=["GET"])
def logout():
    try:
        user, token = verify_token()
        db_ops.logout(token)
        return {"message": "Successfully logged out"}
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception "+str(e)}, 500
