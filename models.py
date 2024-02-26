from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    app.app_context().push()
    db.init_app(app)


"""Models for Blogly."""

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True, )

    first_name = db.Column(db.Text,
                           nullable = False)
    last_name = db.Column(db.Text,
                          nullable = False)
    image_url = db.Column(db.Text, default='https://www.dogster.com/wp-content/uploads/2013/09/australian-shepherd-dog-sitting-on-a-rock-in-the-park_ChocoPie_Shutterstock.jpg.webp')

    post = db.relationship('Post', backref='user', cascade="all,delete")
    
    
class Post(db.Model):
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key = True,
                   nullable = False,
                   autoincrement = True)
    title = db.Column(db.Text,
                      nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
