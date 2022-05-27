#initial blueprint setup
from lib2to3.pgen2 import token
from flask import Blueprint, jsonify,request

api = Blueprint('api',__name__,url_prefix='/api')

#imports for api routes
from app.models import Animal,db,Swans
from .services import token_required

#initial testing route
@api.route('/test', methods = ['GET'])
def test():
    fox = Animal.query.all([0])

    #jsonify creates json from python data
    #we can return a status code alongside this
    # x = Animal.query.all()##This doesnt work!  
    return jsonify(fox.to_dict()),200

#The purpose of this API is going to be to hold a database of porducts that we will use on our mock ecommerce store that we will create in React
#We are making a CRUD API that can create read update and/or delete animals from our database

#1. Setup our Animal Model so that it can hold all the data we need
#2. Set up routing here in our API so that an API request can:
    # read all animal data [GET]
    # read a single animal's data based on their ID [GET]
    # create a new animal [POST]
    # modify an existing animals attributes [POST]
    # delete an animal [DELETE]
##Each of these will be its own route!!
#3. Protecting our API (auth system)

@api.route('/animals',methods = ['GET'])
def getAnimals():
    """
    [GET] Retrieves all animal objects from our database and returns them as JSON data.
    Here, we wont get any additional information with the request, just query to retrieve all animals
    """
    animals = Animal.query.all()
    #we cannot directly jsonify a python object.
    # so we need to transform this list of animals into either a list of dicitonaries, or some similar structure
    animals=[a.to_dict() for a in animals]#list comprehension version
    animals={a.species: a.to_dict() for a in animals}#dictionary comprehension version
    return jsonify(animals)


@api.route('/create',methods=["POST"])
@token_required
def createAnimal():
    """
    ['POST'] create a new animal in our database with data 
    We want the user to pass in a dictionary in the body of the request
    we will access that dictionary and use it to instantiate an instance of an Animal object
    then save that animal object to our database
    and tell our user that the operation was successful
    expected input:
        {
            'species':string
            'description':string
            price:numeric
            all other kv pairs are optional
            latin name:string
            image: string
            size: int
            diet: string
            lifespan:string
        }
    """
    try:   
        newdict = request.get_json()
        print(newdict)
        
        a=Animal(newdict)
    except:
        return jsonify({'error':'improper request or body data'}),400
    try:
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error':'species already exists in the database'}),400
    return jsonify({'created':a.to_dict()}),200


@api.route('/animal<string:name>',methods = ['GET'])
def getAnimalName(name):
    """
    [GET] retrieving a single animal from the database based on that animals name
    so we will get an animal name in from the dynamic route URL,
    query the db for that animal, and return if it exists
    """
    print(name)

    animal = Animal.query.filter_by(species=name.title()).first()
    if animal:
        return jsonify(animal.to_dict()), 200
    #otherwise return an error message
    return jsonify({'error':f'The name {name.title()} does not exist in the database.'}),400


@api.route('/update/<string:id>',methods= ['POST'])
@token_required
def updateAnimal(id):   
    """
    ['POST']Updates an existing animal in our database with data provided in the request body.

    expected input JSON:
        {
        #ALL K:V pairs optional, must have at least one
            'species':string
            'description':string
            price:numeric
            all other kv pairs are optional
            latin name:string
            image: string
            size: int
            diet: string
            lifespan:string
        }
        """
    

    try:
        newvals = request.get_json()
        animal=Animal.query.get(id)
        animal.from_dict(newvals)
        db.session.commit()
        return jsonify({'Updated Animal': animal.to_dict()})
    except:
        return jsonify({'Request failed':'Invalid request or animal ID does not exist.'}),400   
    
    
@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def removeAnimal(id):
    """
    [DELETE]  accepts an animal ID - if that ID exists in the database, remove that animal and return the removed animal object
    """

    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'Remove Failed': f'No animal with ID {id} in the database.'}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'Removed animal': animal.to_dict()}),200

"""
###########################################################################################################
Swans API Routes
###########################################################################################################
"""

@api.route('/swans',methods = ['GET'])
def getSwans():

    swans = Swans.query.all()
    #we cannot directly jsonify a python object.
    # so we need to transform this list of animals into either a list of dicitonaries, or some similar structure
    swans=[a.to_dict() for a in swans]#list comprehension version
    return jsonify(swans)


@api.route('/swans/<string:last_name>',methods = ['GET'])
def getSwanData(last_name):
    swan = Swans.query.filter_by(last_name=last_name.title()).first()
    if swan:
        return jsonify(swan.to_dict()), 200
    #otherwise return an error message
    return jsonify({'error':f'The name {last_name.title()} does not exist in the database.'}),400



@api.route('/create',methods=["POST"])
def createSwan():
    try:   
        newdict = request.get_json()
        print(newdict)
        
        a=Swans(newdict)
    except:
        return jsonify({'error':'improper request or body data'}),400
    try:
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error':'species already exists in the database'}),400
    return jsonify({'created':a.to_dict()}),200

@api.route('/delete/<string:id>', methods=['DELETE'])
def removeSwan(id):
    swan = Swans.query.get(id)
    if not swan:
        return jsonify({'Remove Failed': f'No Swan with ID {id} in the database.'}), 404
    db.session.delete(swan)
    db.session.commit()
    return jsonify({'Removed swan': swan.to_dict()}),200