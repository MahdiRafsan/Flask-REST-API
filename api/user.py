import jwt
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask.helpers import make_response
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

user = Blueprint("user", __name__, url_prefix="/api")

@user.route("/login")
def login():
    """
    user login
    :return: json
    """
    auth = request.authorization

    if not auth or not auth["username"] or not auth["password"]:
        return make_response(str("Could not verify!"), 401, {"WWW-Authenticate": "Basic relam='Login Required!"})

    user = User.query.filter_by(name=auth["username"]).first()
    if not user:
        return make_response("Could not verify!", 401, {"WWW-Authenticate": "Basic relam='Login Required!"})
        
    if check_password_hash(user.password, auth["password"]):
        payload = {"public_id": user.public_id, 
                   "exp": datetime.utcnow() + timedelta(minutes=30)}
        
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        return make_response(jsonify({"token": token}), 201)
    
    return make_response("Could not verify!", 401, {"WWW-Authenticate": "Basic realm='Wrong Password!'"})

@user.route("/sign-up", methods=["POST"]) 
def sign_up():
    """
    create/register a new user
    :return: json
    """
    data = request.get_json()
    hash_pass = generate_password_hash(data["password"], method="sha256")
    
    # first user is created as admin
    if User.query.filter_by(id=1).count() == 0:
            user = User(public_id = str(uuid.uuid4()), password=hash_pass, name = data["name"], admin=True)
    else:
        user = User(public_id = str(uuid.uuid4()), password=hash_pass, name = data["name"], admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "New user has been created!"})


def token_required(f):
    """
    decorator for verifying the jwt
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        # 401 error returned if token is not passed in the header
        if not token:
            return jsonify({"message": "No token found!"}), 401
        
        # get stored info by decoding the payload
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Invalid Token!"}), 401
        
        # return current logged in user context
        return f(current_user, *args, **kwargs)
    
    return wrapper

@user.route("/user", methods = ["GET"])
@token_required
def get_users(current_user):
    """
    get all users
    :param current_user: user currently logged in
    :return: json
    """

    if not current_user.admin:
        return jsonify({"message": "You don't have permission to perform that function!"})

    users = User.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data["public_id"] = user.public_id
        user_data["name"] = user.name
        user_data["password"] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)
    
    return jsonify({"users" : output})

@user.route("/user/<user_id>", methods = ["GET"])
@token_required
def get_user(current_user, user_id):
    """
    get a user by querying from database
    :param current_user: user currently logged in
    :param user_id: str representing public id
    :return: json 
    """
    if not current_user.admin:
        return jsonify({"message": "You don't have permission to perform that function!"})

    user = User.query.filter_by(public_id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"})
    user_data = dict()
    user_data["public_id"] = user.public_id
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["admin"] = user.admin
    output = [user_data]
    return jsonify({"user": output})


@user.route("/user/<user_id>/promote", methods=["PUT"])
@token_required
def promote_user(current_user, user_id):
    """
    promote an existing user to admin
    :param current_user: user currently logged in
    :param user_id: str representing public id
    :return: json
    """
    if not current_user.admin:
        return jsonify({"message": "You don't have permission to perform that function!"})
    
    user = User.query.filter_by(public_id=user_id).first()
    
    if not user:
        return jsonify({"message": "User does not exist!"})
    
    user.admin = True
    db.session.commit()
    return jsonify({"message": "User has been promoted to admin!"})

@user.route("/user/<user_id>/update", methods = ["PUT"])
@token_required
def update_user(current_user, user_id):
    """
    update info about an user
    :param current_user: user currently logged in
    :param user_id: str representing public id
    :return: json
    """
    
    if not current_user.admin:
        return jsonify({"message": "You don't have permission to perform that function!"})
    
    user = User.query.filter_by(public_id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"})

    data = request.get_json()
    user.name = data["name"]
    user.password= generate_password_hash(data["password"], method="sha256")

    db.session.commit()

    return jsonify({"message": "User info has been updated!"})

@user.route("/user/<user_id>", methods=["DELETE"])
@token_required
def remove_user(current_user, user_id):
    """
    delete a user
    :param current_user: user currently logged in
    :param user_id: str representing public id
    :return: json
    """
    if not current_user.admin:
        return jsonify({"message": "You don't have permission to perform that function!"})
    
    user = User.query.filter_by(public_id=user_id).first()
    if not user:
        return jsonify({"message": "User does not exist!"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User has been deleted!"})


