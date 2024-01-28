import unittest
from models.question import Question

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.question = Question()

    def tearDown(self):
        pass

    def test_QuestionID(self):
        # Test the QuestionID attribute
        self.assertIsNone(self.question.QuestionID)
        self.question.QuestionID = "12345"
        self.assertEqual(self.question.QuestionID, "12345")

    def test_QuestionText(self):
        # Test the QuestionText attribute
        self.assertIsNone(self.question.QuestionText)
        self.question.QuestionText = "Test Question"
        self.assertEqual(self.question.QuestionText, "Test Question")

    def test_Options(self):
        # Test the Options attribute
        self.assertIsNone(self.question.Options)
        options = ["Option 1", "Option 2", "Option 3"]
        self.question.Options = options
        self.assertEqual(self.question.Options, options)

    def test_survey_id(self):
        # Test the survey_id attribute
        self.assertIsNone(self.question.survey_id)
        self.question.survey_id = "67890"
        self.assertEqual(self.question.survey_id, "67890")

    def test_Rand_options(self):
        # Test the Rand_options attribute
        self.assertFalse(self.question.Rand_options)
        self.question.Rand_options = True
        self.assertTrue(self.question.Rand_options)

    def test_survey(self):
        # Test the survey relationship
        self.assertIsNone(self.question.survey)
        survey = Survey()
        self.question.survey = survey
        self.assertEqual(self.question.survey, survey)

if __name__ == '__main__':
    unittest.main()