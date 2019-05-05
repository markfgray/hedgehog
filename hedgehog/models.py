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