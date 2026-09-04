from flask import Blueprint, request
from uuid import uuid4
from ..Classes.User import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


user_database = []


def find_user(email):
    for user in user_database:
        if user.email == email:
            return user
    return None

@auth_blueprint.post("/register")
def handle_register():
    user_data = request.get_json(silent=True) or {}
    username = user_data.get("username")
    email = user_data.get('email')
    password = user_data.get('password')
    role = user_data.get('role', 'user')
    new_user = User(
        id=str(uuid4()),
        username=username,
        email=email,
        password=password,
        role=role
    )
    user_database.append(new_user)
    return {"message": "User creation successful"}, 201


@auth_blueprint.post("/login")
def handle_login():
    email = request.json.get('email')
    password = request.json.get('password')

    found_user = None
    for user in user_database:
        if user.email == email and user.password == password:
            found_user = user
            break

    if not found_user:
        return "Invalid credentials", 400

    token = create_access_token(identity=email)
    return {
        "token": token,
        "email":email,
        "status":"Login Successful"
    }, 201


@auth_blueprint.get("/me")
@jwt_required()
def handle_me():
    email = get_jwt_identity()

    found_user = find_user(email)
    
    if not found_user:
        return "Hacker situation", 400

    user = found_user.get_dictionary()
    del user['password']
    return user
