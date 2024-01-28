import unittest
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base_model = BaseModel()

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(self.base_model, BaseModel)
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_save(self):
        old_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(old_updated_at, self.base_model.updated_at)

    def test_to_dict(self):
        base_model_dict = self.base_model.to_dict()
        self.assertIsInstance(base_model_dict, dict)
        self.assertIn('__class__', base_model_dict)
        self.assertEqual(base_model_dict['__class__'], 'BaseModel')
        self.assertIn('id', base_model_dict)
        self.assertEqual(base_model_dict['id'], self.base_model.id)
        self.assertIn('created_at', base_model_dict)
        self.assertEqual(base_model_dict['created_at'], self.base_model.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self.assertIn('updated_at', base_model_dict)
        self.assertEqual(base_model_dict['updated_at'], self.base_model.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))

    def test_delete(self):
        self.base_model.delete()
        # Add assertions here to check if the instance is deleted from the storage

if __name__ == '__main__':
    unittest.main()