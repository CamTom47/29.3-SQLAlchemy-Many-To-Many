from app import app
from unittest import TestCase
from models import Users, Post, db
from random import choice

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

def get_user_id():
    ids = []
    users = Users.query.all()
    for user in users:
        ids.append(user.id)
    return choice(ids)

def get_post_id():
    ids = []
    posts = Post.query.all()
    for post in posts:
        ids.append(post.id)
    return choice(ids)

db.drop_all()
db.create_all()

class BloglyViewsTestCase(TestCase):
    """Class representing test views for blogly web app"""

    def Setup(self):
        """Clean up existing users and posts"""

    Post.query.delete()
    Users.query.delete()

    user1 = Users(first_name='Joe', last_name='Stephenson')
    user2 = Users(first_name='Tim', last_name='Devon')
    user3 = Users(first_name='Allen', last_name='Smith')
    post1 = Post(title='Test Title', content='Test content', user_id=1)
    post2 = Post(title='Test Title2', content='Test content2', user_id=2)
    post3 = Post(title='Test Title3', content='Test content3', user_id=3)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

    def tearDown(self):
        """Clean up any messed up requests"""
        db.session.rollback()

    def test_homepage_redirect(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            id = get_user_id()
            resp = client.get(f'/users/{id}')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)

    def test_show_add_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Enter User Information</h1>', html)

    def test_show_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            id = get_user_id()
            resp = client.post(f'/users/{id}/delete')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_show_user_edit_page(self):
        with app.test_client() as client:
            id = get_user_id()
            resp = client.get(f'/users/{id}/edit')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<label for="last_name">Last Name</label>', html)

    def test_update_user_page(self):
        with app.test_client() as client:
            id = get_user_id()
            resp = client.post(f'/users/{id}/edit', follow_redirects=True, data={'first_name': 'Cameron','last_name': 'Thomas', 'image_url':'None'})
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_show_post_create_page(self):
        with app.test_client() as client:
            id = get_user_id()
            user = Users.query.get(id)
            resp = client.get(f'/users/{id}/posts/new')
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'Add Post for {user.first_name} {user.last_name}', html)

    # def test_update_post(self):
    #     with app.test_client() as client:
    #         post_id = get_post_id()
    #         post = Post.query.get(post_id)
    #         user_id = post.user.id
    #         user = Users.query.get(user_id)
    #         d = {f'title': 'Updated Title', 'content': 'updated content', 'user_id': {user_id}}
    #         resp = client.post(f'/posts/{post_id}/edit', follow_redirects=True, data = d)
    #         html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(f'<p class="fst-italic">{user.first_name} {user.last_name}</p>', html)
    
    def test_delete_post(self):
        with app.test_client() as client:
            post_id = get_post_id()
            user_id = Post.query.get(post_id).user.id
            user = Users.query.get(user_id)
            resp = client.post(f'/posts/{post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'<p class="fw-bold fs-4 d-block">{user.first_name} {user.last_name}</p>', html)

