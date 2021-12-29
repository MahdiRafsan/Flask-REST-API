from flask import Blueprint, request, jsonify
from .models import ToDo
from . import db
from .user import token_required

todo = Blueprint("todo", __name__, url_prefix="/api")

@todo.route("/todo", methods=["POST"])
@token_required
def create_todo(current_user):
    """
    create a new todo
    :param current_user: user currently logged in
    :return: json 
    """
    data = request.get_json()
    
    todo = ToDo(item=data["item"], user_id=current_user.id, complete=False)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "New todo created!"})

@todo.route("/todo", methods=["GET"])
@token_required
def get_todos(current_user):
    """
    get all todos created by a user
    :param current_user: user currently logged in
    :return: json 
    """
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    output = []

    for todo in todos:
        todo_data = {}
        todo_data["id"] = todo.id
        todo_data["item"] = todo.item
        todo_data["complete"] = todo.complete
        output.append(todo_data)

    return jsonify({"todos": output})

@todo.route("/todo/<todo_id>", methods = ["GET"])
@token_required
def get_todo(current_user, todo_id):
    """
    get a todo
    :param current_user: user currently logged in
    :param todo_id: int 
    :return: json 
    """
    todo = ToDo.query.filter_by(id = todo_id).first()

    if not todo:
        return jsonify({"message": "Todo does not exist!"})

    elif not todo.user_id == current_user.id:
        return jsonify({"message": "You don't have permission to perform that function!"})

    todo_data = {}
    todo_data["id"] = todo.id
    todo_data["item"] = todo.item
    todo_data["complete"] = todo.complete
    output = [todo_data]

    return jsonify({"todo": output})

@todo.route("/todo/<todo_id>", methods=["PUT"])
@token_required
def complete_todo(current_user, todo_id):
    """
    mark a todo as completed
    :param current_user: user currently logged in
    :param todo_id: int 
    :return: json 
    """
    todo = ToDo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"message": "Todo does not exist!"})

    elif not todo.user_id == current_user.id:
        return jsonify({"message": "You don't have permission to perform that function!"})

    todo.complete = True
    db.session.commit()

    return jsonify({"message": "Todo item has been updated as complete!"})

@todo.route("/todo/<todo_id>", methods=["DELETE"])
@token_required
def delete_todo(current_user, todo_id):
    """
    delete a todo
    :param current_user: user currently logged in
    :param todo_id: int
    :return: json 
    """
    
    todo = ToDo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"message": "Todo does not exist!"})
    
    elif not todo.user_id == current_user.id:
        return jsonify({"message": "You don't have permission to perform that function!"})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo item deleted!"})