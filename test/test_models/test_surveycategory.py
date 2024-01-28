import unittest
from models.surveycategory import SurveyCategory
from models.survey import Survey
from models.customcategory import CustomCategory
from datetime import datetime

class TestSurveyCategory(unittest.TestCase):
    def setUp(self):
        self.survey_category = SurveyCategory()

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(self.survey_category, SurveyCategory)
        self.assertIsInstance(self.survey_category.SurveyCategoryID, str)
        self.assertIsInstance(self.survey_category.SurveyID, str)
        self.assertIsInstance(self.survey_category.category_id, str)
        self.assertIsInstance(self.survey_category.created_at, datetime)
        self.assertIsInstance(self.survey_category.updated_at, datetime)

    def test_relationships(self):
        self.assertIsInstance(self.survey_category.survey, Survey)
        self.assertIsInstance(self.survey_category.category, CustomCategory)

    def test_to_dict(self):
        survey_category_dict = self.survey_category.to_dict()
        self.assertIsInstance(survey_category_dict, dict)
        self.assertIn('__class__', survey_category_dict)
        self.assertEqual(survey_category_dict['__class__'], 'SurveyCategory')
        self.assertIn('SurveyCategoryID', survey_category_dict)
        self.assertEqual(survey_category_dict['SurveyCategoryID'], self.survey_category.SurveyCategoryID)
        self.assertIn('SurveyID', survey_category_dict)
        self.assertEqual(survey_category_dict['SurveyID'], self.survey_category.SurveyID)
        self.assertIn('category_id', survey_category_dict)
        self.assertEqual(survey_category_dict['category_id'], self.survey_category.category_id)
        self.assertIn('created_at', survey_category_dict)
        self.assertEqual(survey_category_dict['created_at'], self.survey_category.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self.assertIn('updated_at', survey_category_dict)
        self.assertEqual(survey_category_dict['updated_at'], self.survey_category.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))

if __name__ == '__main__':
    unittest.main()