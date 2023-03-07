# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialise the database and file name variables
appDB = SQLAlchemy()
DB_NAME = "assetManagerDatabase.db"

# Function to create the app
def create_app():
    # No parameters
    # Returns 1: app which is the flask web application creates
    # This functions purpose is to set up and create the asset manager web application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "wiuvbisv7374yg438h$%^&"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    appDB.init_app(app)

    from .views import views
    from .auth import auth

    # Register blueprints for webapp routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    # Call the create_database function and pass parameter app
    create_database(app)

    # Set up the login manager for users
    login_manager = LoginManager()
    login_manager.login_view = "views.homePage"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database
def create_database(app):
    # 1 parameter: app as the flask web application made
    # Returns 0 but creates the database
    # This functions purpose is to create the database if one does not already exist

    # Check if the database does not already exists
    if not path.exists("webApp/" + DB_NAME):
        # If the database does not already exist then create the database
        appDB.create_all(app=app)
        print("Database Created")