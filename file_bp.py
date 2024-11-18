from flask import Blueprint, request, send_file

from auth import verify_token
from database import UserDB, FileDB
import db_ops
from exceptions import CustomExceptions

file_bp = Blueprint("file_bp", __name__, url_prefix="/files")

@file_bp.route("/")
def files():
    try:
        user, token = verify_token()
        return db_ops.get_files(user)
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception "+str(e)}, 500
    
@file_bp.route("/add", methods=["POST"])
def add_file():
    try:
        user, token = verify_token()
        if "file" not in request.files:
            raise CustomExceptions("Invalid request", 400)
        data = request.form
        name = data.get("name", "").strip()
        name = name or None
        if name is None:
            raise CustomExceptions("Name is missing", 400)
        file = request.files["file"]
        db_ops.add_file(user, name, file)
        return {"message": "Successfully added the file"}
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception "+str(e)}, 500
    

@file_bp.route("/filedd")
def get_file():
    return send_file("./files/3_1.pdf")