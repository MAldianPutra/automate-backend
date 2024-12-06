from . import db

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(100))

# Add more models as needed
