import unittest
from flask import current_app
from project import create_app, db
from project.models import User
from werkzeug.security import check_password_hash


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": 'sqlite://'} )
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_homepage_redirect(self):
        response = self.client.get('/restaurant', follow_redirects = True)
        assert response.status_code == 200

    def test_sql_injection(self):
        response = self.client.post('/restaurant/new', data = {
            'name' : 'Mcdonalds"; drop table user; -- '
        }, follow_redirects = True)
        assert response.status_code == 200

    def test_xss_vulnerability(self):
        response = self.client.post('/restaurant/new', data = {
            'name' : '<script>alert("test user")</script>',
        }, follow_redirects = True)
        assert response.status_code == 200 
# signs up a new user
    def test_register_user(self):
        response = self.client.post('/signup', data = {
            'email' : 'JohnSmith@test.com',
            'name' : 'John Smith',
            'password' : 'test123'
        }, follow_redirects = True)
        assert response.status_code == 200
        assert response.request.path == '/login'
# redirects to login, and logsin with new user
        response = self.client.post('/login', data = {
            'email' : 'JohnSmith@test.com',
            'password' : 'test123'
        }, follow_redirects = True)
        assert response.status_code == 200
# redirects to profile to find name on screen
        html = response.get_data(as_text = True)
        assert 'John Smith' in html