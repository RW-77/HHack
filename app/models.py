from . import db # import from (within) package
from flask_login import UserMixin
from sqlalchemy.sql import func

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_generated = db.Column(db.DateTime(timezone=True), default=func.now)
    data = db.Column(db.JSON) # schedule
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin): # define table models
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    schedule = db.relationship('Schedule')