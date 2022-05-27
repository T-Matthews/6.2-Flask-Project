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

# Create our user model
class User(db.Model, UserMixin):
    id = db.Column(db.String(40),primary_key=True)
    username=db.Column(db.String(40), nullable = False, unique = True)
    email=db.Column(db.String(100), nullable = False, unique = True)
    password= db.Column(db.String(255),nullable=False)
    bio=db.Column(db.String(255),default='No bio.')
    first_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    created= db.Column(db.DateTime, default = datetime.now())#not needed in init because of default value.
    api_token = db.Column(db.String(100))
    posts = db.relationship('Post',backref='post_author') #tells usermodel that it has a relationship with the Post model

    def __init__(self,username,email,password,first_name,last_name):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = str(uuid4())#UUID is a UUID object, not string. Need to convert.
        self.password = generate_password_hash(password)

#Post model - one User can have many Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow())
    author = db.Column(db.String,db.ForeignKey('user.id'))#creates a foreign key to another db.Model

class Animal(db.Model):
    #global attributes for each column in the database
    id = db.Column(db.String(40),primary_key=True) #we need to provide at least a datatype (we can also provide default values and/or constraints)
    species = db.Column(db.String(50), nullable = False, unique=True)
    latin_name = db.Column(db.String(255), default =None)
    size_cm = db.Column(db.String(255))
    diet = db.Column(db.String(255))
    lifespan = db.Column(db.String(255))  
    description = db.Column(db.String(255), nullable = False)
    image = db.Column(db.String(255), default = None)
    price = db.Column(db.Float(2),nullable = False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    #when a user submits a POST request to CREATE a new Animal, we want to use this __init__ method to handle the animal creation

    def __init__(self, dict):
        #some of these values are required
        self.id = str(uuid4())
        self.species = dict['species'].title()
        self.description = dict['description']
        self.price = dict['price']
        #some are optional
        self.image = dict.get('image')
        self.size_cm = dict.get('size_cm',0)
        self.latin_name = dict.get('latin_name','unknown')[0].upper() + dict.get('latin_name', 'unknown')[1:].lower()
        self.diet= dict.get('diet','unknown')
        self.lifespan = dict.get('lifespan',0)




    #write a function to translate this object to a dictionary for jsonification
    #the other advantage to writing this function is that we can purposely not include some attributes if we dont want them
    def to_dict(self):
        return {
                'id':self.id,
                'species':self.species,
                'image' : self.image,
                'description':self.description,
                'price': self.price,
                'image': self.image,
                'size_cm':self.size_cm,
                'latin_name': self.latin_name,
                'diet':self.diet,
                'lifespan':self.lifespan,
                'created on':self.created_on
        }

# Accepts a dictionary containing attributs that should be changed, then goes 
#       and changes whichever attributes are present in the dictionary
def from_dict(self,dict):    
    for key in dict:
        setattr(self,key,dict[key])


class Swans(db.Model):
    id = db.Column(db.String(40),primary_key=True)
    player_number=db.Column(db.SmallInteger, nullable = False)
    player_position=db.Column(db.String(255), nullable = False)
    first_name=db.Column(db.String(100), nullable = False)
    last_name=db.Column(db.String(100), nullable = False)
    nationality=db.Column(db.String(20))
    previous_club=db.Column(db.String(40),default='Unknown previous club info')
    created= db.Column(db.DateTime, default = datetime.now())#not needed in init because of default value.

    def __init__(self,dict):
        self.player_position = dict['player_position']
        self.player_number = dict['player_number']
        self.first_name = dict['first_name'].title()
        self.last_name = dict['last_name'].title()
        self.nationality= dict.get('nationality','Unknown').title()
        self.prevous_club = dict.get('previous_club','Unknown').title()
        self.id = str(uuid4())#UUID is a UUID object, not string. Need to convert.

    def to_dict(self):
        return {
            'player_position': self.player_position,
            'player_number': self.player_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nationality':self.nationality,
            'id':self.id
        }