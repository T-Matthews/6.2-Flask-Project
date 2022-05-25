#This file is responsible for everything database
#Primarily instantiation of ORM (object relational mapper), as well as creation of our database

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask_login import LoginManager,UserMixin
login=LoginManager()

#tell our login manager how it can access a user object from a user_id
@login.user_loader
def load_user(userid):
    return User.query.get(userid)




from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash

#create a DB model -> aka a python object that will be a table in our sql database
class Animal(db.Model):
    #global attributes for each column in the database
    id = db.Column(db.Integer,primary_key=True) #we need to provide at least a datatype (we can also provide default values and/or constraints)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(255), default =None)
    created = db.Column(db.DateTime, default = datetime.now())
    cool = db.Column(db.Boolean, default=True)


# Create our user model
class User(db.Model, UserMixin):
    id = db.Column(db.String(40),primary_key=True)
    username=db.Column(db.String(40), nullable = False, unique = True)
    email=db.Column(db.String(100), nullable = False, unique = True)
    password= db.Column(db.String(255),nullable=False)
    first_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    created= db.Column(db.DateTime, default = datetime.now())#not needed in init because of default value.

    def __init__(self,username,email,password,first_name,last_name):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = str(uuid4())#UUID is a UUID object, not string. Need to convert.
        self.password = generate_password_hash(password)



        