from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()


class Employees(db.Model):
    """This model is for our table"""
    __tablename__='employees'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    gender = db.Column(db.String(25))
    city = db.Column(db.String(125))


    def __init__(self, name, gender, city):
        self.name = name
        self.gender = gender
        self.city = city




    

