import unittest
from api.models import User
from test.basic import Base

class TestAuth(Base):
    """
    test authorization functionalities
    """
    def test_sign_up(self):
        """
        test sign-up route with multiple users
        """
        res = self.sign_up("name", "12345")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["message"], "New user has been created!")

        res = self.sign_up("username", "12345")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["message"], "New user has been created!")

        user1 = User.query.filter_by(name="name").first()
        user2 = User.query.filter_by(name="username").first()
        self.assertTrue(user1.admin == 1)
        self.assertTrue(user2.admin == 0)

    def test_login(self):
        """
        test login route with correct info
        """
        self.sign_up("username", "password")
        res = self.login("username", "password")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(str, type(res.json["token"]))
        self.assertEqual(res.content_type, "application/json")

    def test_login_wrong_username(self):
        """
        test login route with wrong username
        """
        self.sign_up("user1", "default")
        response = self.login("user", "password")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_data(as_text=True), "Could not verify!")

    def test_login_wrong_password(self):
        """
        test login route with wrong password
        """
        self.sign_up("user1", "default")
        response = self.login("user1", "password")
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Could not verify!", response.data)

if __name__ == "__main__":
    unittest.main()