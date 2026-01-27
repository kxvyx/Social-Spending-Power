from fastapi import APIRouter
from app.models import Bill, bill_dict

router = APIRouter(prefix="/users/{id}/bills", tags=["bills"])

@router.get("/")
def get_user_bills(id:int):
    return "show all bills of user {id}"