from app import app
from unittest import TestCase

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BloglyViewsTestCase(TestCase):
    """Class representing test views for blogly web app"""

    def test_homepage_redirect(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get('/users/4')
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