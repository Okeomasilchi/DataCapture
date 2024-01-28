import unittest
from models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(UserID="12345", FirstName="John", Email="john@example.com", Password="password", LastName="Doe")

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.UserID, "12345")
        self.assertEqual(self.user.FirstName, "John")
        self.assertEqual(self.user.Email, "john@example.com")
        self.assertEqual(self.user.Password, "password")
        self.assertEqual(self.user.LastName, "Doe")

    def test_user_surveys_relationship(self):
        self.assertIsInstance(self.user.user_surveys, list)
        self.assertEqual(len(self.user.user_surveys), 0)

    def test_user_surveys_backref(self):
        survey = Survey(user=self.user, Title="Test Survey", Description="This is a test survey")
        self.assertEqual(len(self.user.user_surveys), 1)
        self.assertEqual(self.user.user_surveys[0], survey)
        self.assertEqual(survey.user, self.user)

if __name__ == '__main__':
    unittest.main()