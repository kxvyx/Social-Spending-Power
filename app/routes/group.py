from fastapi import APIRouter, Response, status, HTTPException
from app.models import Group,GroupUpdate
from app.utils.db_populate import bill_dict, user_dict, group_dict
from datetime import datetime

router = APIRouter(prefix="/users/{user_id}", tags=["groups"])

@router.get("/groups", status_code=200)
def get_user_groups(user_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    all_user_groups = {}
    for group_id , group_data in group_dict.items():
       if group_data.user_id == user_id:
        all_user_groups[group_id] =group_data
    return all_user_groups

@router.get("/groups/{group_id}", status_code=200)
def get_user_group_by_id(user_id:int,group_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    if group_dict[group_id].user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot access since user id doesnt match"
        )
    return group_dict[group_id]

@router.post("/groups", status_code=201)
def create_group(user_id:int , group:Group):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    if group.user_id != user_id:
        raise HTTPException(
            status_code=403, detail = "Group user id does not match with the user"
        )
    
    group_dict[group.group_id] = group
    return group

@router.patch("/groups/{group_id}" , status_code=200)
def update_group(user_id:int , group_id:int , group:GroupUpdate):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group_dict[group_id].user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id}, not authorized to update"
        )
    stored_group_data = group_dict[group_id]
    update_data = group.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now()
    updated_data = stored_group_data.model_copy(update=update_data)
    group_dict[group_id] = updated_data
    return group_dict[group_id]

@router.delete("/groups/{group_id}" , status_code=204)
def delete_group(user_id:int , group_id:int ):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group_dict[group_id].user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id}, not authorized to delete"
        )
    del group_dict[group_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# for bill in group functions

@router.post("/groups/{group_id}" , status_code=201)
def add_bill_to_group(user_id:int,group_id:int,bill_id:int):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    if bill_id not in bill_dict:
        raise HTTPException(status_code=404, detail="Bill not found")
    if bill_dict[bill_id].user_id != user_id and group_dict[group_id].user_id != user_id :
        raise  HTTPException(status_code=403, 
                             detail=f"User {user_id}, not authorized to add this bill")

    group_obj = group_dict[group_id]
    if bill_id in group_obj.list_of_bills:
        return "Bill already exists in this group"
    
    group_obj.list_of_bills.append(bill_id)
    group_obj.cost += bill_dict[bill_id].cost
    group_dict[group_id].updated_at = datetime.now()
    return group_obj
    
# write function to get bills in a group -> 
@router.get("/groups/{group_id}/bills" , status_code=200)
def get_list_of_bills(user_id:int,group_id:int):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    
    list_of_bills = group_dict[group_id].list_of_bills
    bills = [bill_dict[bill_id] for bill_id in list_of_bills]
    return bills


@router.delete("/groups/{group_id}/bills/{bill_id}" , status_code=204)
def delete_bill_from_group(user_id:int,group_id:int,bill_id:int):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    if group_id not in group_dict:
        raise HTTPException(status_code=404, detail="Group not found")
    if bill_id not in bill_dict:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    bill_owner_id = bill_dict[bill_id].user_id
    group_owner_id = group_dict[group_id].user_id
    if user_id != bill_owner_id and user_id != group_owner_id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user_id} is not authorized to delete this bill"
        )
    list_of_bills = group_dict[group_id].list_of_bills
    if bill_id in list_of_bills:
        list_of_bills.remove(bill_id)
        group_dict[group_id].cost -= bill_dict[bill_id].cost
        group_dict[group_id].updated_at = datetime.now()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Bill {bill_id} not found in the group {group_id}"
        )
    