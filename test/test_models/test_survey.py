import unittest
from models.survey import Survey
from models.user import User
from models.question import Question
from models.response import Response
from datetime import datetime, date

class TestSurvey(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.survey = Survey(user=self.user, Title="Test Survey", Description="This is a test survey", ExpiryDate=date.today(), Visibility=True, Randomize=False, QuestionsType="Multiple Choice")

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsInstance(self.survey, Survey)
        self.assertIsInstance(self.survey.SurveyID, str)
        self.assertIsInstance(self.survey.user_id, str)
        self.assertEqual(self.survey.user_id, self.user.UserID)
        self.assertEqual(self.survey.Title, "Test Survey")
        self.assertEqual(self.survey.Description, "This is a test survey")
        self.assertIsInstance(self.survey.created_at, datetime)
        self.assertIsInstance(self.survey.updated_at, datetime)
        self.assertEqual(self.survey.ExpiryDate, date.today())
        self.assertEqual(self.survey.Visibility, True)
        self.assertEqual(self.survey.Randomize, False)
        self.assertEqual(self.survey.QuestionsType, "Multiple Choice")

    def test_relationships(self):
        self.assertIsInstance(self.survey.user, User)
        self.assertEqual(self.survey.user, self.user)
        self.assertIsInstance(self.survey.questions, list)
        self.assertEqual(len(self.survey.questions), 0)
        self.assertIsInstance(self.survey.responses, list)
        self.assertEqual(len(self.survey.responses), 0)

    def test_add_question(self):
        question = Question(survey=self.survey, Text="What is your favorite color?")
        self.survey.questions.append(question)
        self.assertEqual(len(self.survey.questions), 1)
        self.assertEqual(self.survey.questions[0], question)
        self.assertEqual(question.survey, self.survey)

    def test_add_response(self):
        response = Response(survey=self.survey, user=self.user, question=None, answer="Blue")
        self.survey.responses.append(response)
        self.assertEqual(len(self.survey.responses), 1)
        self.assertEqual(self.survey.responses[0], response)
        self.assertEqual(response.survey, self.survey)

if __name__ == '__main__':
    unittest.main()