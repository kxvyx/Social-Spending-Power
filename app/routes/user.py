from app.models import User, UserModel, UserUpdate
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
    user_dict[user.user_id] = user
    return user

@router.patch("/users/{user_id}", status_code=200)
def update_user(user_id:int,user:UserUpdate):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if user_dict[user_id].user_id != user_id:
        raise  HTTPException(status_code=403, 
                             detail=f"User {user_id}, not authorized to update")
    stored_user_data = user_dict[user_id]
    update_data = user.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now()
    updated_user = stored_user_data.model_copy(update=update_data)

    user_dict[user_id] = updated_user
    return user_dict[user_id]

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id:int):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if user_dict[user_id].user_id != user_id:
        raise  HTTPException(status_code=403, 
                             detail=f"User {user_id}, not authorized to delete")
    
    remove_bills = [bill_id for bill_id in bill_dict if bill_dict[bill_id].user_id == user_id]
    groups = [group_id for group_id in group_dict if group_dict[group_id].user_id == user_id]
    bills_in_groups = []
    for group_id,group_obj in group_dict.items():
        for bill_id in group_obj.list_of_bills:
            if bill_dict[bill_id].user_id == user_id:
                group_obj.cost -= bill_dict[bill_id].cost
                group_obj.list_of_bills.remove(bill_id)
    for bill_id in remove_bills:
        del bill_dict[bill_id]    
    for group_id in groups:
        del group_dict[group_id]
    del user_dict[user_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    