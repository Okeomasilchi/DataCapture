import unittest
from models.engine.db_storage import DBStorage
from models.customcategory import CustomCategory
from models.question import Question

class TestDBStorage(unittest.TestCase):
    def setUp(self):
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        self.db.close()

    def test_all(self):
        # Test retrieving all objects of a specific class
        all_custom_categories = self.db.all(CustomCategory)
        self.assertIsInstance(all_custom_categories, dict)
        self.assertEqual(len(all_custom_categories), 0)

    def test_new(self):
        # Test adding a new object to the database session
        question = Question()
        self.db.new(question)
        self.assertIn(question, self.db._DBStorage__session.new)

    def test_save(self):
        # Test committing changes to the database session
        question = Question()
        self.db.new(question)
        self.db.save()
        self.assertIn(question, self.db._DBStorage__session)

    def test_delete(self):
        # Test deleting an object from the database session
        question = Question()
        self.db.new(question)
        self.db.save()
        self.db.delete(question)
        self.assertNotIn(question, self.db._DBStorage__session)

    def test_get(self):
        # Test retrieving an instance of a class by its ID
        question = Question()
        self.db.new(question)
        self.db.save()
        retrieved_question = self.db.get(Question, question.id)
        self.assertEqual(retrieved_question, question)

    def test_count(self):
        # Test counting the number of objects in a class
        question1 = Question()
        question2 = Question()
        self.db.new(question1)
        self.db.new(question2)
        self.db.save()
        self.assertEqual(self.db.count(Question), 2)

if __name__ == '__main__':
    unittest.main()