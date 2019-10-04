from hedgehog import db
from werkzeug import generate_password_hash, check_password_hash

class RegisterInterest(db.Model):
    __tablename__ = 'registerinterest'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email
        }

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    placetype = db.Column(db.String())
    placename = db.Column(db.String())

    def __init__(self, email, placetype, placename):
        self.email = email
        self.placetype = placetype
        self.placename = placename

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'placetype': self.placetype,
            'placename': self.placename
        }

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    placename = db.Column(db.String())
    rater = db.Column(db.String())
    rating = db.Column(db.Integer)
    date = db.Column(db.String())
    comment = db.Column(db.String())

    def __init__(self, placename, rater, rating, date, comment):
        self.placename = placename
        self.rater = rater
        self.rating = rating
        self.date = date
        self.comment = comment

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    pwdhash = db.Column(db.String())
    created_on = db.Column(db.String())
    last_login = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    def __init__(self, email, username, password, created_on, last_login, first_name, last_name):
        self.email = email
        self.username = username
        self.set_password(password)
        self.created_on = created_on
        self.last_login = last_login
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    

