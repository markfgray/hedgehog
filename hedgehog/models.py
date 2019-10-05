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
    __tablename__ = 'establishments'

    eid = db.Column(db.Integer, primary_key=True)
    establishment_type = db.Column(db.String())
    name = db.Column(db.String())
    latitude = db.Column(db.Numeric())
    longitude = db.Column(db.Numeric())
    facilities = db.Column(db.String())

    def __init__(self, establishment_type, name, latitude, longitude, facilities):
        self.establishment_type = establishment_type
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.facilities = facilities

    def __repr__(self):
        return '<eid {}>'.format(self.eid)

class Rating(db.Model):
    __tablename__ = 'ratings'

    rid = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    rater = db.Column(db.String())
    placename = db.Column(db.String())
    rating = db.Column(db.Integer)
    pros = db.Column(db.String())
    cons = db.Column(db.String())
    eid = db.Column(db.Integer)

    def __init__(self, date, rater, placename, rating, pros, cons, eid):
        self.date = date
        self.rater = rater
        self.rating = rating
        self.placename = placename
        self.pros = pros
        self.cons = cons
        self.eid = eid

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
        return '<id {}>'.format(self.user_id)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    

