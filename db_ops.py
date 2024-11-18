
import hashlib
from sqlalchemy import select

from auth import generate_token
from database import UserDB, FileDB, BlacklistTokens, db
from exceptions import CustomExceptions


UPLOAD_FOLDER = "./files/"

# Auth Related
def login(username: str, password: str):
    stmt = select(UserDB).where(UserDB.username == username)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomExceptions("User does not exist", 400)
    user: UserDB = rows[0]
    password = hashlib.md5(password.encode()).hexdigest()
    if user.password != password:
        raise CustomExceptions("Invalid password", 400)
    token = generate_token(user)
    return {"access_token": token}

def register(user: UserDB):
    stmt = select(UserDB).where(UserDB.username == user.username)
    rows = db.session.execute(stmt).one_or_none()
    if rows is not None:
        raise CustomExceptions("Username already exists", 400)
    user.password = hashlib.md5(user.password.encode()).hexdigest()
    db.session.add(user)
    db.session.commit()

def logout(token: str):
    blacklist = BlacklistTokens(token)
    db.session.add(blacklist)
    db.session.commit()

def get_files(user: UserDB):
    stmt = select(FileDB).where(FileDB.userId == user.id)
    rows = db.session.execute(stmt).all()
    files = []
    for file in rows:
        print(type(file[0]))
        files.append(file[0].toJson())
    return {"files": files}

def add_file(user: UserDB, name: str, file):
    stmt = select(UserDB).where(UserDB.id == user.id)
    rows = db.session.execute(stmt).one_or_none()
    if not rows:
        raise CustomExceptions("Invalid user", 401)
    user = rows[0]
    files_len = len(user.files)
    if "." not in file.filename or file.filename.count(".")>1:
        raise CustomExceptions("No extension of file", 400)
    ext = file.filename.split(".")[1]
    filename = UPLOAD_FOLDER+f"{str(user.id)}_{str(files_len)}.{ext}"
    file.save(filename)
    file = FileDB(name, filename, userId=user.id)

    db.session.add(file)
    db.session.commit()


