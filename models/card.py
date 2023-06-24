from init import db, ma
from marshmallow import fields

class Card(db.Model):
    
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='cards')
    comments = db.relationship('Comment', back_populates='card')

class CardSchema(ma.Schema):
    # Tell Marshmallow to use UserSchema to serialize the 'User' field
    user = fields.Nested('UserSchema', exclude=['password'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['card', 'id']))


    class Meta:
        fields = ('id', 'title', 'description', 'status', 'user', 'comments')
        ordered = True