from app.models import User, UserModel
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from app.models import user_dict
from datetime import datetime

router = APIRouter(tags=["users"])

@router.get("/users/")
def get_all_users():
    return user_dict

@router.get("/users/{id}")
def get_user_by_id(id:int):
    if id not in user_dict:
        return "User not found"
    return user_dict[id]

@router.post("/users/")
def create_user(user: User):
    user_dict[user.user_id] = jsonable_encoder(user)
    return "created new user"

@router.patch("/users/{id}")
def update_user(id:int,user:User):
    if id not in user_dict:
        return "user not found"
    stored_user = user_dict[id]
    stored_user_data = User(**stored_user)

    update_data = user.model_dump(exclude_unset=True)
    updated_user = stored_user_data.model_copy(update=update_data)

    user_dict[id] = jsonable_encoder(updated_user)
    return "updated successfully"

@router.delete("/users/{id}")
def delete_user(id:int):
    if id in user_dict:
        del user_dict[id]
        return "user deleted successfully"
    else:
        return "user not found"