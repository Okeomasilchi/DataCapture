import unittest
from models.response import Response

class TestResponse(unittest.TestCase):
    def setUp(self):
        self.response = Response()

    def tearDown(self):
        pass

    def test_ResponseID(self):
        # Test the ResponseID attribute
        self.assertIsNone(self.response.ResponseID)
        self.response.ResponseID = "12345"
        self.assertEqual(self.response.ResponseID, "12345")

    def test_responders_bio(self):
        # Test the responders_bio attribute
        self.assertIsNone(self.response.responders_bio)
        self.response.responders_bio = {"name": "John", "age": 25}
        self.assertEqual(self.response.responders_bio, {"name": "John", "age": 25})

    def test_Timestamp(self):
        # Test the Timestamp attribute
        self.assertIsNone(self.response.Timestamp)
        self.response.Timestamp = "2022-01-01 12:00:00"
        self.assertEqual(self.response.Timestamp, "2022-01-01 12:00:00")

    def test_Answers(self):
        # Test the Answers attribute
        self.assertIsNone(self.response.Answers)
        self.response.Answers = {"question1": "answer1", "question2": "answer2"}
        self.assertEqual(self.response.Answers, {"question1": "answer1", "question2": "answer2"})

    def test_SurveyID(self):
        # Test the SurveyID attribute
        self.assertIsNone(self.response.SurveyID)
        self.response.SurveyID = "67890"
        self.assertEqual(self.response.SurveyID, "67890")

    def test_survey(self):
        # Test the survey relationship
        self.assertIsNone(self.response.survey)
        survey = Survey()
        self.response.survey = survey
        self.assertEqual(self.response.survey, survey)

if __name__ == '__main__':
    unittest.main()