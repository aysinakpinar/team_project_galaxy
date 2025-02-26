from models import UserModel
from extension import db
from datetime import date
from faker import Faker

factory = Faker()
#Aysin's code for testing creating users
def create_user(username=None, email=None, location=None):
    if username is None:
        username = factory.name()
    if email is None:
        email = factory.email() 
    if location is None:
        location = factory.city()  
        
    user = UserModel(
        username=username,
        password="password123",
        email=email,
        location=location
    )
    
    db.session.add(user)
    db.session.commit()
    return user
