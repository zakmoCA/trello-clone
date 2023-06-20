from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy 
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app.debug = True

app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

db = SQLAlchemy(app)
ma= Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401) 

@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You must be an admin'}, 401

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'password', 'is_admin')

class Card(db.Model):
    
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'date_created')
        ordered = True

@app.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('spinynorman').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='cleese@spam.com',
            password=bcrypt.generate_password_hash('tisbutascratch').decode('utf-8')
        )
    ]
    
    # Create an instance of the Card model in memory
    cards = [
        Card(
        title = 'Start the project',
        description = 'Stage 1 - Create an ERD',
        # Create an ERC
        status = 'Done',
        date_created = date.today()
        ),
        Card(
        title = 'ORM Queries',
        description = 'Stage 2 - Implement several queries',
        status = 'In progress',
        date_created = date.today()
        ),
        Card(
        title = 'Marshmallow',
        description = 'Stage 3 - Implement jsonify of mdoels',
        status = 'In progress',
        date_created = date.today()
        ),
    ]
    # Truncate the Card table
    db.session.query(Card).delete()
    db.session.query(User).delete()
    
    # Add the card to the session (transaction)
    db.session.add_all(cards)
    db.session.add_all(users)
    

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')

@app.route('/register', methods=['POST'])
def register():
    try:
        # Parse, sanitize and validate the incoming JSON data
        # via the schema
        user_info = UserSchema().load(request.json)
        # Create a new User model instance with the schema data
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
            name=user_info['name']
        )

        # Add and commit the new user
        db.session.add(user)
        db.session.commit()

        # Return the new user, excluding the password
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409
    
@app.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400


@app.route('/cards')
@jwt_required()
def all_cards():
    admin_required()

    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

@app.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)