from domains.generative_ai import GenerativeAI
from schemas.quiz.request import GradeQuizRequest
from domains import prompt_builder


class QuizGrader:
    def __init__(self, request: GradeQuizRequest):
        self.source_language = request.source_language
        self.target_language = request.target_language
        self.difficulty = request.difficulty
        self.quiz = request.quiz
        self.user_input_code = request.user_input_code

    def grade_quiz(self):
        # prompt build
        prompt = prompt_builder.build_prompt(
            template="grade_quiz.txt",
            replacements={
                "source_language": self.source_language,
                "target_language": self.target_language,
                "difficulty": self.difficulty,
                "quiz": self.quiz,
                "user_input_code": self.user_input_code,
            }
        )

        #call bedrock
        bedrock = GenerativeAI()
        response = bedrock.invoke_model(prompt)

        return response

        