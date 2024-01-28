import unittest
from models.customcategory import CustomCategory

class TestCustomCategory(unittest.TestCase):
    def setUp(self):
        self.custom_category = CustomCategory()

    def tearDown(self):
        pass

    def test_CategoryID(self):
        # Test the CategoryID attribute
        self.assertIsNone(self.custom_category.CategoryID)
        self.custom_category.CategoryID = "12345"
        self.assertEqual(self.custom_category.CategoryID, "12345")

    def test_CategoryName(self):
        # Test the CategoryName attribute
        self.assertIsNone(self.custom_category.CategoryName)
        self.custom_category.CategoryName = "Test Category"
        self.assertEqual(self.custom_category.CategoryName, "Test Category")

    def test_UserID(self):
        # Test the UserID attribute
        self.assertIsNone(self.custom_category.UserID)
        self.custom_category.UserID = "67890"
        self.assertEqual(self.custom_category.UserID, "67890")

    def test_user(self):
        # Test the user relationship
        self.assertIsNone(self.custom_category.user)
        user = User()
        self.custom_category.user = user
        self.assertEqual(self.custom_category.user, user)

if __name__ == '__main__':
    unittest.main()