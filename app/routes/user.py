from app.models import User, UserModel
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Response, status, HTTPException
from app.utils.db_populate import user_dict,bill_dict,group_dict
from datetime import datetime

router = APIRouter(tags=["users"])

@router.get("/users", status_code=200)
def get_all_users():
    return user_dict

@router.get("/users/{user_id}", status_code=200)
def get_user_by_id(user_id:int):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user_dict[user_id]

@router.post("/users" ,status_code=201 )
def create_user(user: User):
    user_dict[user.user_id] = jsonable_encoder(user)
    return user

@router.patch("/users/{user_id}", status_code=200)
def update_user(user_id:int,user:User):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    stored_user = user_dict[user_id]
    stored_user_data = User(**stored_user)

    update_data = user.model_dump(exclude_unset=True)
    updated_user = stored_user_data.model_copy(update=update_data)

    user_dict[user_id] = jsonable_encoder(updated_user)
    return user_dict[user_id]

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id:int):
    if user_id in user_dict:
        remove_bills = [bill_id for bill_id in bill_dict if bill_dict[bill_id].get("user_id") == user_id]
        groups = [group_id for group_id in group_dict if group_dict[group_id].get("user_id") == user_id]
        for bill_id in remove_bills:
            del bill_dict[bill_id]    
        for group_id in groups:
            del group_dict[group_id]
        del user_dict[user_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )