from pydantic import BaseModel, EmailStr,Field
from datetime import date

class User(BaseModel):
    id: int
    name: str = Field(max_length=30,description="Name of user")
    email: EmailStr
    phone_no: int = Field( description="Phone no. of user")
    salary: float = Field(gt=0)

class Bill(BaseModel):
    id: int
    type: str = Field(max_length=30,description="Type of bill")
    description: str = Field(max_length=60,description="Description of bill")
    is_paid: bool = False
    cost: float = Field(gt=0)
    due_date: date

class Event(BaseModel):
    id: int
    event_name: str = Field(max_length=30,description="name of event")
    description: str = Field(max_length=60,description="Description of event")
    cost: float = Field(gt=0)
    event_date: date