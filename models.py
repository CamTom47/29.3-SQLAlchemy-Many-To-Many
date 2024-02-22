from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    app.app_context().push()
    db.init_app(app)


"""Models for Blogly."""

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)

    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text)
    
