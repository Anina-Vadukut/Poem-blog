from db import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user_detail'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(120))
    password = db.Column(db.String(20))
    
    def __init__(self, username, email, password):
         self.username = username
         self.email = email
         self.password = password


    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

