#Were going to be building a token required decorator
#Essentially, this will perform the same role for API routes that the Login_required decorator performs for tempated routes

#General structure of a custom decorator:
#a closure -> defining a function inside of another function where the inner function is returned by the outer function

#outer function with the name of the custom decorator
    # @wraps()
    #inner function
        #code to run before the decorated function runs
        #can either return the decorated function (causing it to run like normal)
        #or return something else, preventing the decorated function from running
    #return the inner function

from flask import request,jsonify
from functools import wraps
from app.models import User, Swans


def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args,**kwargs):
        #code here will run before the decorated function(the api route) runs
        #try to get the access token
        token = request.headers.get('foxes-access-token')
        #if there is no token - stop the request and send a forbidden message
        if not token:
            return jsonify({'Access denied':'No API Token - please register to receive your API token.'}),401
            #Wont make it to the bottom return statement, so the request will be stopped.
        #if there is a token - check validity. If not valid, stop the request and send a forbidden message
        if not User.query.filter_by(api_token=token).first():
            return jsonify({'Invalid API Token':'Please verify token or request a new one.'}),403
        #if the token is present and valid, allow the request to go through
        return api_route(*args,**kwargs)#returns call to outermost function
    return decorator_function