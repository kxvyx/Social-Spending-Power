from fastapi import FastAPI
from app.models import User
from app.routes import user
from app.routes import bill


app = FastAPI()
app.include_router(user.router)
app.include_router(bill.router)


@app.get("/")
def root():
    return "this is homepage..."