from db import db

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    poem = db.Column(db.Text())
    key = db.Column(db.String(100))
    
    def __init__(self, title, poem, key):
        self.title = title
        self.poem = poem
        self.key = key