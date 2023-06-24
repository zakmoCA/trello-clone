from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.card import Card
from models.comment import Comment
from datetime import date

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')

@cli_bp.cli.command('seed')
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

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()
    
    # Create an instance of the Card model in memory
    cards = [
        Card(
        title = 'Start the project',
        description = 'Stage 1 - Create an ERD',
        # Create an ERC
        status = 'Done',
        date_created = date.today(),
        user_id=users[0].id #admin is first in our users list so this will be admin
        ),
        Card(
        title = 'ORM Queries',
        description = 'Stage 2 - Implement several queries',
        status = 'In progress',
        date_created = date.today(),
        user_id=users[0].id #admin is first in our users list so this will be admin
        ),
        Card(
        title = 'Marshmallow',
        description = 'Stage 3 - Implement jsonify of mdoels',
        status = 'In progress',
        date_created = date.today(),
        user_id=users[1].id #John Cleese is cecond in our users list so this will be John
        ),
    ]
    # Truncate the Card table
    db.session.query(Card).delete()
    
    # Add the card to the session (transaction)
    db.session.add_all(cards)
    
    # Commit the transaction to the database
    db.session.commit()

    comments = [
        Comment(
            message='Comment 1',
            date_created=date.today(),
            user_id=users[0].id,
            card_id=cards[1].id
        ),
        Comment(
            message='Comment 2',
            date_created=date.today(),
            user_id=users[1].id,
            card_id=cards[1].id
        ),
        Comment(
            message='Comment 3',
            date_created=date.today(),
            user_id=users[1].id,
            card_id=cards[0].id
        )
    ]
    # Truncate the Comment table
    db.session.query(Comment).delete()
    
    # Add the comment to the session (transaction)
    db.session.add_all(comments)
    
    # Commit the transaction to the database
    db.session.commit()

    print('Models seeded')
