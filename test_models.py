from unittest import TestCase
from app import app
from models import db, Users, Post

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UsersModelTestCase(TestCase):

    def Setup(self):
        """Clean up existing users and posts"""

        Users.query.delete()
        Post.query.delete()
        db.session.commit()

    def tearDown(self):
        """Clean up any messed up requests"""
        db.session.rollback()

    def test_user_get_by(self):
        user = Users(first_name='Joe', last_name='Stephenson')
        self.assertEqual(user.first_name, 'Joe')
    
    
class PostModelTestCase(TestCase):
    
    def Setup(self):
        """Clean up existing users and posts"""

        Users.query.delete()
        Post.query.delete()
        db.session.commit()

    def tearDown(self):
        """Clean up any messed up requests"""
        db.session.rollback()

    def test_user_post_relation(self):
        post = Post(title='Test Title', content='Test content', user_id=1)
        self.assertEqual(post.user_id, 1)


class TagModelTestCase(TestCase):


class PostTagModelTestCase(TestCase):