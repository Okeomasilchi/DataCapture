import unittest
from models.engine.file_storage import FileStorage
from models.customcategory import CustomCategory
from models.question import Question

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.storage.reload()

    def tearDown(self):
        self.storage.close()

    def test_all(self):
        # Test retrieving all objects of a specific class
        all_custom_categories = self.storage.all(CustomCategory)
        self.assertIsInstance(all_custom_categories, dict)
        self.assertEqual(len(all_custom_categories), 0)

    def test_new(self):
        # Test adding a new object to the storage
        question = Question()
        self.storage.new(question)
        key = question.__class__.__name__ + "." + question.id
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_save(self):
        # Test saving objects to the JSON file
        question = Question()
        self.storage.new(question)
        self.storage.save()
        with open(self.storage._FileStorage__file_path, 'r') as f:
            json_objects = json.load(f)
        key = question.__class__.__name__ + "." + question.id
        self.assertIn(key, json_objects)

    def test_reload(self):
        # Test reloading objects from the JSON file
        question = Question()
        self.storage.new(question)
        self.storage.save()
        self.storage.reload()
        key = question.__class__.__name__ + "." + question.id
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_delete(self):
        # Test deleting an object from the storage
        question = Question()
        self.storage.new(question)
        self.storage.save()
        self.storage.delete(question)
        key = question.__class__.__name__ + "." + question.id
        self.assertNotIn(key, self.storage._FileStorage__objects)

    def test_get(self):
        # Test retrieving an instance of a class by its ID
        question = Question()
        self.storage.new(question)
        self.storage.save()
        retrieved_question = self.storage.get(Question, question.id)
        self.assertEqual(retrieved_question, question)

    def test_count(self):
        # Test counting the number of objects in a class
        question1 = Question()
        question2 = Question()
        self.storage.new(question1)
        self.storage.new(question2)
        self.storage.save()
        self.assertEqual(self.storage.count(Question), 2)

if __name__ == '__main__':
    unittest.main()