import unittest, json
from main import app
from extensiones import db
from models import Juego # Ajustado para importar correctamente tu modelo

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Como no usamos create_app, configuramos la app que ya existe en main.py
        app.config['TESTING'] = True
        # MUY IMPORTANTE: Usamos una base de datos temporal en memoria para no borrar tus datos reales
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
        
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        db.create_all()
        db.session.add(Juego(nombre='X', descripcion='Y', precio=1.23))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all() 
        self.ctx.pop()

    def test_get_juegos(self):
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()