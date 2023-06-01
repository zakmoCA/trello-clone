from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import date
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello_clone'

db = SQLAlchemy(app)

class Card(db.Model):
    
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

@app.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')

@app.cli.command('seed')
def seed_db():
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
    
    # Add the card to the session (transaction)
    db.session.add_all(cards)
    

    # Commit the transaction to the database
    db.session.commit()
    print('Models seeded')



@app.cli.command('all_cards')
def all_cards():
    # select * from cards;
    stmt = db.select(Card).where(Card.status != 'Done', Card.id > 2)
    cards = db.session.scalars(stmt).all()
    for card in cards:
        print(card.__dict__)

@app.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)