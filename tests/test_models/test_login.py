import unittest
import bcrypt
from models.user_login import Login  # Replace with the actual module name

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        # Hash a password for testing
        self.password = 'secure_password'
        self.hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        self.email = 'test@example.com'
        self.login = Login(self.email, self.hashed_password)

    def test_email(self):
        """Test that the email is stored in lowercase."""
        self.assertEqual(self.login.email, self.email.lower())

    def test_verify_user_success(self):
        """Test successful user verification."""
        result = self.login.verify_user(self.email, self.password)
        self.assertTrue(result)

    def test_verify_user_wrong_email(self):
        """Test user verification with incorrect email."""
        result = self.login.verify_user('wrong@example.com', self.password)
        self.assertFalse(result)

    def test_verify_user_wrong_password(self):
        """Test user verification with incorrect password."""
        result = self.login.verify_user(self.email, 'wrong_password')
        self.assertFalse(result)

    def test_repr(self):
        """Test the __repr__ method."""
        expected_repr = f"<Login(email={self.email.lower()}, password={'*' * 60})>"
        self.assertEqual(repr(self.login), expected_repr)

if __name__ == '__main__':
    unittest.main()
