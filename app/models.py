from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, func, Date
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr,Field
from datetime import date
from typing import Optional

engine = create_engine("sqlite:///project_database.db",echo=True)


class User(BaseModel):
    user_id: int
    name: str = Field(max_length=30,description="Name of user")
    email: EmailStr
    phone_no: int = Field( description="Phone no. of user")
    salary: float = Field(gt=0)
    created_at: datetime = Field(default_factory =datetime.now)
    updated_at: datetime = Field(default_factory =datetime.now)

class Bill(BaseModel):
    bill_id: int
    user_id: int = Field(description="user id of this bill")
    type: str = Field(max_length=30,description="Type of bill")
    description: str = Field(max_length=60,description="Description of bill")
    is_paid: bool = False
    cost: float = Field(gt=0)
    due_date: date
    created_at: datetime = Field(default_factory =datetime.now)
    updated_at: datetime = Field(default_factory =datetime.now)

class Event(BaseModel):
    event_id: int
    event_name: str = Field(max_length=30,description="name of event")
    description: str = Field(max_length=60,description="Description of event")
    cost: float = Field(gt=0)
    event_date: date
    created_at: datetime = Field(default_factory =datetime.now)
    updated_at: datetime = Field(default_factory =datetime.now)


class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__= "user_info"

    user_id: Mapped[int] = mapped_column(primary_key=True) #id INTEGER NOT NULL
    name: Mapped[str] = mapped_column(String(30)) #name VARCHAR(30) NOT NULL
    email: Mapped[str]  #email_address VARCHAR NOT NULL
    phone_no: Mapped[int] 
    salary: Mapped[float] 
    bills: Mapped[list["BillModel"]] = relationship(back_populates="bill_owner")
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    updated_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), onupdate=func.current_date())


class BillModel(Base):
    __tablename__= "bills"

    bill_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))
    type: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(50))
    is_paid: Mapped[bool] = mapped_column(default=False)
    cost: Mapped[float]
    due_date: Mapped[date]
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    updated_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), onupdate=func.current_date())
    bill_owner: Mapped["UserModel"] = relationship(back_populates="bills")

class EventModel(Base):
    __tablename__= "events"

    event_id: Mapped[int] = mapped_column(primary_key=True)
    event_name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(50))
    cost: Mapped[float]
    event_date: Mapped[date]
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    updated_at: Mapped[date] = mapped_column(Date, server_default=func.current_date(), onupdate=func.current_date())

if __name__=="__main__":
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        shinchan = UserModel(name="Shinchan", email="shinchan@gmail.com",phone_no=1234567890,salary=10000)
        batman = UserModel(name="Batman", email="iambatman@gmail.com",phone_no=9876543210,salary=90000)
        jane = UserModel(name="Jane", email="jane@gmail.com", phone_no=7896456676, salary=800000)
        bob = UserModel(name="Bob", email="bobbyy@gmail.com", phone_no=2395479845, salary=1000000)
        ryu = UserModel(name="Ryu", email="ruru@gmail.com", phone_no=9665894343, salary=600000)

        session.add_all([shinchan,batman,jane,bob,ryu])
        session.commit()
        print("Database created and users added!")

'''For now ive kept these dictionaries here, import clashes ho rahe the
is there a better place to keep them?'''

user_dict = {
    1:User(user_id=1, name="Jane", email="jane@gmail.com", phone_no=7896456676, salary=800000),
    # 2:User(user_id=2, name="Bob", email="bobbyy@gmail.com", phone_no=2395479845, salary=1000000),
    # 3:User(user_id=3, name="Ryu", email="ruru@gmail.com", phone_no=9665894343, salary=600000)
}

bill_dict = {
    # bill_id: {bill} object
}