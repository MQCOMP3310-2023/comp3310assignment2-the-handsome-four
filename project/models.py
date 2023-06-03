from . import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class MenuItem(db.Model):
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id'))
    restaurant = db.    relationship(Restaurant)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'       : self.name,
           'description' : self.description,
           'id'         : self.id,
           'price'      : self.price,
           'course'     : self.course,
       }

class User(UserMixin,db.Model):
    name = db.Column(db.String(20), nullable = False)
    u_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

    def get_id(self):
        return (self.u_id)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'              : self.name,
           'u_id'                : self.u_id,
           'email'             : self.email,    
           'password'          : self.password, 
       }

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    r_id = db.Column(db.Integer, ForeignKey(Restaurant.id))
    u_id = db.Column(db.Integer, ForeignKey(User.u_id))
    score = db.Column(db.Float)

    def get_id(self):
        return (self.rating_id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'rating_id'     :self.rating_id,
            'r_id'            :self.r_id,
            'u_id'          :self.u_id,
            'score'         :self.score,
        }
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    restaurant = db.relationship('Restaurant', backref=db.backref('bookings', lazy=True))
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'              : self.id,
           'restaurant_id'   : self.restaurant_id,
           'user_id'         : self.user_id,
           'booking_time'    : self.booking_time,
       }