from typing import Optional
from flask import Blueprint, request, send_file, current_app

from auth import verify_token
from database import UserDB, FileDB
import db_ops
from exceptions import CustomExceptions

file_bp = Blueprint("file_bp", __name__, url_prefix="/files")

@file_bp.route("/")
@file_bp.route("/<fileId>")
def files(fileId: Optional[int] = None):
    current_app.logger.debug("Hi from files")
    try:
        user, token = verify_token()
        if fileId is None:
            return db_ops.get_files(user)
        url = db_ops.get_file(user, fileId)
        return send_file(url)
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
    
@file_bp.route("/change", methods=["PUT"])
def putName():
    try:
        user, token = verify_token()
        data = request.get_json()
        fileId = data.get("fileId", "")
        if type(fileId) == str:
            fileId = fileId.strip()
            if fileId.isnumeric():
                fileId = int(fileId)
            else:
                raise CustomExceptions("Invalid file id", 400)
        elif type(fileId) != int:
            raise CustomExceptions("Invalid fileId", 400)
        name = data.get("name", "").strip()
        db_ops.update_file(user, fileId, name)
        return {"message": "Successfully updated file"}
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500
    
@file_bp.route("/delete/<fileId>", methods=["DELETE"])
def delete(fileId: int):
    try:
        user, token = verify_token()
        db_ops.delete_file(user, fileId)
        return {"message": "Successfully deleted"}
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500