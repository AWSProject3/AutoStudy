import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app
from schemas.quiz.response import GenerateQuizResponse, HintDetails, CategoryDetails
from models.repository import QuizRepository


class TestGenerateQuizHandler(unittest.TestCase):

    @patch('api.quiz.QuizService.create_quiz')
    @patch('api.quiz.QuizRepository')
    def test_generate_quiz_handler(self, mock_quiz_repo, mock_create_quiz):
        # mock response from QuizService
        mock_response = GenerateQuizResponse(
            source_language="test",
            target_language="test",
            difficulty="easy",
            category=CategoryDetails(type="test", detail="detail for test"),
            quiz="quiz for test",
            hint=HintDetails(source_language_code="test", describe="describe for test"),
            answer="answer for test"
        )
        mock_create_quiz.return_value = mock_response

        # Request payload
        payload = {
            "source_language": "test",
            "target_language": "test",
            "difficulty": "easy"
        }

        # set up FastAPI TestClient
        client = TestClient(app)

        # mock QuizRepository
        mock_quiz_repo.return_value = MagicMock(spec=QuizRepository)

        # post request to /api/quiz/generate endpoint
        response = client.post("/api/quiz/generate", json=payload)

        # test
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), mock_response.dict())
        mock_create_quiz.assert_called_once()

if __name__ == "__main__":
    unittest.main()
