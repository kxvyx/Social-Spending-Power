from sqlalchemy.orm import Session
from app.models import engine, Base, UserModel,User

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



user_dict = {
    1:User(user_id=1, name="Jane", email="jane@gmail.com", phone_no=7896456676, salary=800000),
    # 2:User(user_id=2, name="Bob", email="bobbyy@gmail.com", phone_no=2395479845, salary=1000000),
    # 3:User(user_id=3, name="Ryu", email="ruru@gmail.com", phone_no=9665894343, salary=600000)
}

bill_dict = {
    # bill_id: {bill} object
}