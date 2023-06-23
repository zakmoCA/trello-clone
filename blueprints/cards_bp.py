from flask import Blueprint, request
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

cards_bp = Blueprint('cards', __name__, url_prefix='/cards') # prefix means we dont have to include 'cards' in our routes

@cards_bp.route('/')
@jwt_required()
def all_cards():
    admin_required()

    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards), 200

#when first creating routes dont worry about auth
@cards_bp.route('/<int:card_id>')
def one_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card is None:
        return{"error": "Card not found"}, 404
    return CardSchema().dump(card)

@cards_bp.route('/create', methods=['POST'])
def create_card():
    # Parse, sanitize and validate the incoming JSON data
    # via the schema
    card_info = CardSchema().load(request.json)
    # Create a new Card model instance with the schema data
    card = Card(
        title=card_info['title'],
        description=card_info['description'],
        status=card_info['status'],
        date_created=date.today(),
        user_id = card_info['user_id']
    )

    # Add and commit the new user
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201


@cards_bp.route('/delete/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card is None:
        return{"error": "Card not found"}, 404
    else:
        print('Card will be deleted')
        db.session.delete(card)
        db.session.commit()
    
    return CardSchema().dump(card), 200