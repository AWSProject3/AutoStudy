import unittest
from unittest.mock import MagicMock, patch

from domains.quiz_generator import QuizGenerator
from models.repository import QuizRepository
from schemas.quiz.request import GenerateQuizRequest
from schemas.quiz.response import CategoryDetails, GenerateQuizResponse, HintDetails
from services.quiz_service import QuizService


class TestQuizService(unittest.TestCase):
    @patch.object(QuizGenerator, 'create_quiz')
    @patch.object(QuizRepository, 'save_quiz')
    def test_create_quiz(self, mock_save_quiz, mock_create_quiz):
        # mock QuizGenerator - create_quiz setting
        mock_response = GenerateQuizResponse(
            source_language="test",
            target_language="test",
            difficulty="easy",
            category=CategoryDetails(type="test", detail="test"),
            quiz="quiz for test code",
            hint=HintDetails(source_language_code="test", describe="test"),
            answer="answer for test code"
        )
        mock_create_quiz.return_value = mock_response

        # mock QuizRepository - save_quiz setting
        mock_save_quiz.return_value = None

        # create GenerateQuizRequest object
        request = GenerateQuizRequest(
            source_language="English",
            target_language="French",
            difficulty="hard"
        )

        # create mock QuizRepository
        mock_session = MagicMock()
        mock_session.commit.return_value = None
        mock_repo = MagicMock(spec=QuizRepository)
        mock_repo.session = mock_session

        # create QuizService
        quiz_service = QuizService(request, mock_repo)

        # call create_quiz method
        response = quiz_service.create_quiz()

        # test QuizGenerator - call create_quiz method
        mock_create_quiz.assert_called_once()

        # test QuizRepository - call save_quiz method
        mock_save_quiz.assert_called_once_with(quiz_data=mock_response)

        # test expected response
        self.assertIsInstance(response, GenerateQuizResponse)

if __name__ == "__main__":
    unittest.main()
