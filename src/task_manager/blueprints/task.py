from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import user_database
from datetime import datetime
from ..Classes.Task import Task
from uuid import uuid4


task_bp = Blueprint("tasks",__name__, url_prefix="/tasks")

task_archive = {}


def current_user():
    email = get_jwt_identity()
    for user in user_database:
        if user.email == email:
            return user
    return None

@task_bp.get("/")
@jwt_required()
def handle_task():
    user = current_user()
    if not user:
        return "Resource not found", 404
    tasks = task_archive.get(user.id, [])
    list_task = list(map(lambda x:x.get_dictionary(), tasks))
    return list_task
    

@task_bp.post("/")
@jwt_required()
def add_task(): 
    body_args=  request.json
    user = current_user()
    if not user:
        return "Resource not found", 404
    task = Task(
            id= f"TASK_ID_{str(uuid4())}",
            title= body_args.get("title"),
            description=body_args.get("description"),
            user_id=user.id,
            created_at=str(datetime.now())
        )
    
    if user.id in task_archive:
        task_archive[user.id].append(task)
    else:
        task_archive[user.id] = [task]


    return {"message":"Task created"}, 201


@task_bp.put("/<task_id>")
@jwt_required()
def handle_update_task(task_id):
    user = current_user()
    if not user:
        return "Resource not found", 404

    body_params = request.get_json(silent=True) or {}
    if not body_params:
        return {"error": "Request body is required"}, 400

    task_list = task_archive.get(user.id, [])

    for task in task_list:
        if task.id == task_id:
            if "title" in body_params:
                if not body_params["title"]:
                    return {"error": "title cannot be empty"}, 400
                task.title = body_params["title"]
            if "description" in body_params:
                task.description = body_params["description"]
            return {
                "message": "Task updated",
                "task": task.get_dictionary(),
            }, 200

    return {"message": "Task not found"}, 404


@task_bp.delete("/<task_id>")
@jwt_required()
def handle_delete_task(task_id):

    user = current_user()
    if not user:
        return {"message": "User not found"}, 404

    task_list = task_archive.get(user.id, [])

    for index, task in enumerate(task_list):
        if task.id == task_id:
            del task_list[index]

            return {"message": "Task deleted successfully"}, 200

    return {"message": "Task not found"}, 404
