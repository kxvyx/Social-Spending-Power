from fastapi import FastAPI
from app.models import User
from typing import Optional

app = FastAPI()

user_dict = {
    1:User(id=1, name="Jane", email="jane@gmail.com", phone_no=7896456676, salary=800000),
    2:User(id=2, name="Bob", email="bobbyy@gmail.com", phone_no=2395479845, salary=1000000),
    3:User(id=3, name="Ryu", email="ruru@gmail.com", phone_no=9665894343, salary=600000)
}

@app.get("/")
def root():
    return "this works..."

@app.get("/users")
def get_all_users():
    return user_dict

@app.get("/users/{id}")
def get_user_by_id(id:int):
    if id not in user_dict:
        return "User not found"
    return user_dict[id]

@app.post("/users")
def create_user(user: User):
    user_dict[user.id] = user
    return "created new user"

@app.patch("/users/{id}")
def update_user(id:int,name: Optional[str]=None,email: Optional[str]=None,phone_no: Optional[int] = None, 
    salary: Optional[float] = None):
    if id not in user_dict:
        return "user not found"
    user = user_dict[id]
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if phone_no is not None:
        user.phone_no = phone_no
    if salary is not None:
        user.salary = salary

    return "updated successfully"

@app.delete("/users/{id}")
def delete_user(id:int):
    if id in user_dict:
        del user_dict[id]
        return "user deleted successfully"
    else:
        return "user not found"