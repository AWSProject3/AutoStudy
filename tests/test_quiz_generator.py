import unittest
from unittest.mock import MagicMock, patch

from domains.generative_ai import GenerativeAI
from domains import prompt_builder
from domains.quiz_generator import QuizGenerator
from schemas.quiz.request import GenerateQuizRequest

class TestQuizGenerator(unittest.TestCase):

    @patch.object(prompt_builder, 'build_prompt')
    @patch.object(GenerativeAI, 'invoke_model')
    def test_create_quiz(self, mock_invoke_model, mock_build_prompt):
        # mock build_prompt setting
        mock_prompt = "{{source_language}} to {{target_language}} in {{difficulty}}"
        mock_build_prompt.return_value = mock_prompt

        # mock invoke_model setting
        mock_response = {"quiz": "generated quiz"}
        mock_invoke_model.return_value = mock_response

        # create GenerateQuizRequest for test
        request = GenerateQuizRequest(
            source_language="test",
            target_language="test",
            difficulty="test"
        )

        # create QuizGenerator
        quiz_generator = QuizGenerator(request)

        # call create_quiz method
        response = quiz_generator.create_quiz()

        # test build_prompt
        mock_build_prompt.assert_called_once_with(
            replacements={
            "source_language": request.source_language,
            "target_language": request.target_language,
            "difficulty": request.difficulty
            }
        )

        # test invoke_model
        mock_invoke_model.assert_called_once_with(mock_prompt)

        # test expected response
        self.assertEqual(response, mock_response)

if __name__ == "__main__":
    unittest.main()
