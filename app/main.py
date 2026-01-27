from fastapi import FastAPI
from app.models import User
from app.routes import user


app = FastAPI()
app.include_router(user.router)

@app.get("/")
def root():
    return "this is homepage..."