from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

VALID_STATUSES = ['To Do', 'Done', 'In Progress', 'Testing', 'Deployed']


class Card(db.Model):
    
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card')

class CardSchema(ma.Schema):
    # Tell Marshmallow to use UserSchema to serialize the 'User' field
    user = fields.Nested('UserSchema', exclude=['password'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['card', 'id']))
    title = fields.String(required=True, validate=And( # And allows multiple validation statements
        Length(min=3, error='Title must be at least 3 characters long'),
        Regexp('^[a-zA-Z0-9]+$', error='Only letters, numbers and spaces are allowed')
    )) # there must be a title field, and it must be a string
    description = fields.String(load_default='')
    status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ('id', 'title', 'description', 'status', 'user', 'comments')
        ordered = True