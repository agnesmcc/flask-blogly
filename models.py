from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()   

def connect_db(app): 
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    posts = db.relationship('Post', backref='user', cascade='all, delete')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        )





