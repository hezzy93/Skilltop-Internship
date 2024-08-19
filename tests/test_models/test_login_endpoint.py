import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from api.v1.app import app  # Replace with the actual module name where your Flask app is defined
from unittest.mock import patch
import bcrypt

class TestLoginEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('models.storage.get_user_by_email')
    @patch('models.user.generate_auth_token')
    def test_login_user_success(self, mock_generate_auth_token, mock_get_user_by_email):
        """Test successful login."""
        mock_user = unittest.mock.Mock()
        mock_user.password = bcrypt.hashpw(b'secure_password', bcrypt.gensalt())
        mock_user.generate_auth_token = mock_generate_auth_token
        mock_generate_auth_token.return_value = 'fake_token'
        mock_get_user_by_email.return_value = mock_user
        
        response = self.app.post('/login', json={
            'email': 'test@example.com',
            'password': 'secure_password'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        self.assertEqual(response.json['message'], 'Successful login')

    @patch('models.storage.get_user_by_email')
    def test_login_user_incorrect_email(self, mock_get_user_by_email):
        """Test login with incorrect email."""
        mock_get_user_by_email.return_value = None
        
        response = self.app.post('/login', json={
            'email': 'wrong@example.com',
            'password': 'secure_password'
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Incorrect email')

    @patch('models.storage.get_user_by_email')
    def test_login_user_incorrect_password(self, mock_get_user_by_email):
        """Test login with incorrect password."""
        mock_user = unittest.mock.Mock()
        mock_user.password = bcrypt.hashpw(b'secure_password', bcrypt.gensalt())
        mock_get_user_by_email.return_value = mock_user
        
        response = self.app.post('/login', json={
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Incorrect Password')

if __name__ == '__main__':
    unittest.main()
