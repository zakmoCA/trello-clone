from flask import Blueprint
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/cards')
@jwt_required()
def all_cards():
    admin_required()

    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

#when first creating routes dont worry about auth
@cards_bp.route('/cards/<int:card_id>')
def one_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card is None:
        return{"error": "Card not found"}, 404
    return CardSchema().dump(card)