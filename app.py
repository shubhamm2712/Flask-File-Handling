from flask import Flask

from auth import verify_token
import auth_bp
import file_bp
from config import config
from database import db
from exceptions import CustomExceptions

app = Flask(__name__)

app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp.bp)
app.register_blueprint(file_bp.file_bp)

@app.route("/")
def home():
    return "Hello"

@app.route("/p")
def private():
    try:
        user, token = verify_token()
        return {"message": "Hello "+user.username}
    except CustomExceptions as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500