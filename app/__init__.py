from flask import Flask, render_template
from config import Config
#any new blueprint needs an import
from .auth.routes import auth
#imports for database stuff. Need ORM, and flask migrate (version control) connected
from .models import db,login
from flask_migrate import Migrate






app = Flask(__name__)

app.config.from_object(Config)


app.register_blueprint(auth) #This line links the app and the blueprint auth

#setup orm and migrate communication with app and eachother
db.init_app(app) #allows for updating database info
migrate = Migrate(app,db)#allows for updating of database structure - new tables,etc.

#setup for LoginManager
login.init_app(app)
login.login_view = 'auth.login'
login.login_message = 'Please log in to tsee this page.'
login.login_message_category = 'danger'


from . import routes