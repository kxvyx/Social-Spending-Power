from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, Integer, String
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr,Field
from datetime import date

engine = create_engine("sqlite:///project_database.db",echo=True)



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







class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__= "user info"

    id: Mapped[int] = mapped_column(primary_key=True) #id INTEGER NOT NULL
    name: Mapped[str] = mapped_column(String(30)) #name VARCHAR(30) NOT NULL
    email: Mapped[str]  #email_address VARCHAR NOT NULL
    phone_no: Mapped[int] 
    salary: Mapped[float] 

    # def __repr__(self) -> str:
    #     return f"User(id={self.id!r}, name={self.name!r}, salary={self.salary!r})"

class BillModel(Base):
    __tablename__= "bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(50))
    cost: Mapped[float]
    isPaid: Mapped[bool] = mapped_column(default=False)
    date: Mapped[date]

class EventModel(Base):
    __tablename__= "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(50))
    cost: Mapped[float]
    date: Mapped[date]

if __name__=="__main__":
    Base.metadata.create_all(engine)
    
    # with Session(engine) as session:
    #     shinchan = User(name="Shinchan", email="shinchan@gmail.com",phone_no=1234567890,salary=10000)
    #     batman = User(name="Batman", email="iambatman@gmail.com",phone_no=9876543210,salary=90000)

    #     session.add_all([shinchan,batman])
    #     session.commit()

