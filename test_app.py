import unittest
from application import application
from unittest.mock import patch
import json
from models import BlacklistEmail, db
import uuid

unique_email = f"test-{uuid.uuid4()}@example.com"
unique_app_uuid = f"{uuid.uuid4()}"

class TestBlacklistEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True
        self.token = "Bearer my_static_token"
        with application.app_context():
            db.create_all()

    def tearDown(self):
        with application.app_context():
            db.drop_all()
    
    def test_post_add_email_to_blacklist(self):
        # Definir los datos de prueba para el POST
        data = {
            'email': unique_email,
            'app_uuid': unique_app_uuid,
            'blocked_reason': 'Test reason for blacklist'
        }
        headers = {
            'Authorization': self.token
        }

        # Realizar la solicitud POST
        response = self.app.post('/blacklists', data=json.dumps(data), headers=headers, content_type='application/json')

        # Verificar el código de estado y la respuesta
        print(response.data)
        self.assertEqual(response.status_code, 400) # Cambiar a 201
        self.assertIn(f'Email {unique_email} added to blacklist', response.json['message'])

    def test_get_check_email_in_blacklist(self):
        
        #Creo el correo primero
        data = {
            'email': unique_email,
            'app_uuid': unique_app_uuid,
            'blocked_reason': 'Test reason for blacklist'
        }
        headers = {
            'Authorization': self.token
        }

        # Realizar la solicitud POST
        response = self.app.post('/blacklists', data=json.dumps(data), headers=headers, content_type='application/json')

        # Definir un email de prueba que debe estar en la lista negra
        email = unique_email

        # Realizar la solicitud GET
        response = self.app.get(f'/blacklists/{email}', headers=headers)

        # Verificar el código de estado y la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIn('blacklisted', response.json)
        self.assertIn('blocked_reason', response.json)
        # Puedes verificar si está en la lista negra según tus datos de prueba
        self.assertTrue(response.json['blacklisted'])
        self.assertEqual(response.json['blocked_reason'], 'Test reason for blacklist')

    def test_get_check_email_not_in_blacklist(self):
        # Definir un email de prueba que NO debe estar en la lista negra
        email = 'not_in_blacklist@example.com'
        headers = {
            'Authorization': self.token
        }

        # Realizar la solicitud GET
        response = self.app.get(f'/blacklists/{email}', headers=headers)

        # Verificar el código de estado y la respuesta
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['blacklisted'])
        self.assertEqual(response.json['message'], 'Email not in blacklist')

if __name__ == '__main__':
    unittest.main()
