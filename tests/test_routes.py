import os
# Engañamos a main.py ANTES de importarlo para que use SQLite (¡Protege tus datos!)
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import unittest
from main import app
from extensiones import db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all() 
        self.ctx.pop()

    def test_index_access(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_profile_requires_login(self):
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

if __name__ == '__main__':
    unittest.main()