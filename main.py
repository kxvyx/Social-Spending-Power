from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import create_engine

engine = create_engine("sqlite:///project_database.db",echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__= "user info"

    id: Mapped[int] = mapped_column(primary_key=True) #id INTEGER NOT NULL
    name: Mapped[str] = mapped_column(String(30)) #name VARCHAR(30) NOT NULL
    email: Mapped[str]  #email_address VARCHAR NOT NULL
    phone_no: Mapped[int] 
    salary: Mapped[float] 

    # def __repr__(self) -> str:
    #     return f"User(id={self.id!r}, name={self.name!r}, salary={self.salary!r})"

if __name__=="__main__":
    Base.metadata.create_all(engine)