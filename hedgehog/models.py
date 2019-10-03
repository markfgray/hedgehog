from hedgehog import db

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
    pwdhash = db.Column(db.String())

    def __init__(self, email, pwdhash):
        self.email = email
        self.pwdhash = pwdhash

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

