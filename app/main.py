from fastapi import FastAPI
from app.routes import user
from app.routes import bill
from app.routes import group


app = FastAPI()
app.include_router(user.router)
app.include_router(bill.router)
app.include_router(group.router)


@app.get("/")
def root():
    return "this is homepage..."