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