from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.cards_bp import cards_bp
from marshmallow.exceptions import ValidationError


#This is a factory function, a function whose job is to create and configure, and return an object
def setup():
    app = Flask(__name__)
    # app.debug = True

    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)


    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        # for production return the messages below
        return {'error': err.__dict__['messages']}, 400 
        # return {'error': err.__dict__}, 400 # for debugging return the entire error

    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cards_bp)

    # Using 'flask run' will run the app as long as this file is called app.py
    # and as long as our code is wrapped inside a 'create_app()' function
    return app
    # When i run this in terminal, set env var = 'FLASK_DEBUG=1 flask run' to run in debug
    # OR create '.flaskenv' file and add FLASK_DEBUG=1

