from fastapi import FastAPI
from pydanticModels import User

app = FastAPI()

user_list = [
    User(id=1, name="Jane", email="jane@gmail.com", phone_no=7896456676, salary=800000),
    User(id=2, name="Bob", email="bobbyy@gmail.com", phone_no=2395479845, salary=1000000),
    User(id=3, name="Ryu", email="ruru@gmail.com", phone_no=9665894343, salary=600000)
]

@app.get("/")
def root():
    return "this works..."

@app.get("/users")
def get_all_users():
    return user_list

@app.get("/users/{id}")
def get_user_by_id(id:int):
    for user in user_list:
        if user.id == id:
            return user
    return "User not found"