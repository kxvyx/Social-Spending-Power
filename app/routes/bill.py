from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.models import Bill, bill_dict, user_dict

#is this the standard way of using apirouter?
router = APIRouter(prefix="/users/{id}", tags=["bills"])

@router.get("/bills")
def get_user_bills(id:int):
    if id not in user_dict:
        return "User not found"
    user_bills = {}
    for bill_id , bill_data in bill_dict.items():
        if bill_data.get("user_id") == id:
            user_bills[bill_id] = bill_data
    return user_bills
     
@router.get("/bill/{bill_id}")
def get_user_bill_by_id(user_id:int,bill_id:int):
    if user_id not in user_dict:
        return "User not found"
    if bill_id not in bill_dict:
        return "Bill not found"
    return bill_dict[bill_id]

@router.post("/bill/")
def create_bill(user_id:int , bill:Bill):
    if user_id in user_dict:
        bill_dict[bill.bill_id] = jsonable_encoder(bill)
        return "Bill successfully created"
    return "User not found"