import os
# Engañamos a main.py ANTES de importarlo para que use SQLite (¡Protege tus datos!)
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import unittest
from main import app
from extensiones import db
from models import Juego # Corregida la ruta del modelo

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all() 
        self.ctx.pop()

    def test_juego_creation(self):
        j = Juego(nombre='Test', descripcion='Desc', precio=9.99)
        db.session.add(j)
        db.session.commit()
        self.assertEqual(Juego.query.count(), 1)

if __name__ == '__main__':
    unittest.main()