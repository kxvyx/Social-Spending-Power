from fastapi import APIRouter, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.models import Bill
from app.utils.db_populate import bill_dict, user_dict

router = APIRouter(prefix="/users/{user_id}", tags=["bills"])

@router.get("/bills", status_code=200)
def get_user_bills(user_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    user_bills = {}
    for bill_id , bill_data in bill_dict.items():
        if bill_data.get("user_id") == user_id:
            user_bills[bill_id] = bill_data
    return user_bills
     
@router.get("/bills/{bill_id}", status_code=200)
def get_user_bill_by_id(user_id:int,bill_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    if bill_id not in bill_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Bill {bill_id} not found"
        )
    if bill_dict[bill_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot access since user id doesnt match"
        )
    return bill_dict[bill_id]

@router.post("/bills", status_code=201)
def create_bill(user_id:int , bill:Bill):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    bill_dict[bill.bill_id] = jsonable_encoder(bill)
    return bill

@router.patch("/bills/{bill_id}" , status_code=200)
def update_bill(user_id:int , bill_id:int , bill:Bill):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if bill_id not in bill_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Bill {bill_id} not found"
        )
    
    if bill_dict[bill_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot update since user id doesnt match"
        )
    stored_bill = bill_dict[bill_id]
    stored_bill_data = Bill(**stored_bill)

    update_data = bill.model_dump(exclude_unset=True)
    updated_data = stored_bill_data.model_copy(update=update_data)
    bill_dict[bill_id] = jsonable_encoder(updated_data)
    return bill_dict[bill_id]

@router.delete("/bills/{bill_id}" , status_code=204)
def delete_bill(user_id:int , bill_id:int ):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if bill_id not in bill_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Bill {bill_id} not found"
        )
    if bill_dict[bill_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot delete since user id doesnt match"
        )
    del bill_dict[bill_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)