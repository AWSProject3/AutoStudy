from domains.quiz_grader import QuizGrader
from interface.impl.cached_quiz import CachedQuizRepository
from models.orm import Grade, Quiz
from schemas.quiz.request import GenerateQuizRequest, GradeQuizRequest
from domains.quiz_generator import QuizGenerator
from schemas.quiz.response import CategoryDetails, FeedbackDetails, GenerateQuizResponse, GradeQuizResponse, HintDetails, ScoreDetails


class QuizService:
    def __init__(self, repo: CachedQuizRepository):
        self.repo = repo

    def create_quiz(self, request: GenerateQuizRequest, user: dict) -> GenerateQuizResponse:
        # generate quiz
        generator = QuizGenerator(request, self.repo, user)
        response = generator.create_quiz()

        # save db & update redis
        db_quiz: Quiz = self.repo.save_quiz(quiz_data=response, user=user)
        
        return GenerateQuizResponse(
            id=db_quiz.id,
            source_language=db_quiz.source_language,
            target_language=db_quiz.target_language,
            difficulty=db_quiz.difficulty,
            category=CategoryDetails(
                type=db_quiz.category_type,
                detail=db_quiz.category_detail
            ),
            quiz=db_quiz.quiz,
            hint=HintDetails(
                source_language_code=db_quiz.hint_source_language_code,
                describe=db_quiz.hint_description
            ),
            answer=db_quiz.answer_code
        )
    
    def grade_quiz(self, request: GradeQuizRequest, user:dict) -> GradeQuizResponse:

        # grade quiz
        grader = QuizGrader(request, self.repo, user)
        response = grader.grade_quiz()

        # save db & update redis
        db_grade: Grade = self.repo.save_grade(grade_data=response, request_data=request, user=user)

        return GradeQuizResponse(
            id=db_grade.id,
            score=ScoreDetails(
                accuracy=db_grade.score.accuracy,
                efficiency=db_grade.score.efficiency,
                readability=db_grade.score.readability,
                pep8_compliance=db_grade.score.pep8_compliance,
                modularity_reusability=db_grade.score.modularity_reusability,
                exception_handling=db_grade.score.exception_handling
            ),
            total_score=db_grade.total_score,
            summary=db_grade.summary,
            detailed_feedback=FeedbackDetails(
                accuracy=db_grade.detailed_feedback.accuracy,
                efficiency=db_grade.detailed_feedback.efficiency,
                readability=db_grade.detailed_feedback.readability,
                pep8_compliance=db_grade.detailed_feedback.pep8_compliance,
                modularity_reusability=db_grade.detailed_feedback.modularity_reusability,
                exception_handling=db_grade.detailed_feedback.exception_handling
            ),
            positive_feedback=db_grade.positive_feedback,
            suggestions=[suggestion.content for suggestion in db_grade.suggestions],
            best_practice_code=db_grade.best_practice_code,
            best_practice_explanation=db_grade.best_practice_explanation
        )
    
    def get_quiz_history(self, user: dict):
        quizzes = self.repo.get_quiz_list(user=user)

        return [GenerateQuizResponse(
            id=quiz.id,
            source_language=quiz.source_language,
            target_language=quiz.target_language,
            difficulty=quiz.difficulty,
            category=CategoryDetails(
                type=quiz.category_type,
                detail=quiz.category_detail
            ),
            quiz=quiz.quiz,
            hint=HintDetails(
                source_language_code=quiz.hint_source_language_code,
                describe=quiz.hint_description
            ),
            answer=quiz.answer_code
        ) for quiz in quizzes]
        
    def get_grade_result(self, quiz_id: int, user: dict) -> GradeQuizResponse | None:
        
        grade = self.repo.get_grade(quiz_id, user)
        
        if grade is None:
            return None
        
        return GradeQuizResponse(
            id=grade.id,
            total_score=grade.total_score,
            summary=grade.summary,
            positive_feedback=grade.positive_feedback,
            best_practice_code=grade.best_practice_code,
            best_practice_explanation=grade.best_practice_explanation,
            score=ScoreDetails(**grade.score.__dict__) if grade.score else ScoreDetails(),
            detailed_feedback=FeedbackDetails(**grade.detailed_feedback.__dict__) if grade.detailed_feedback else FeedbackDetails(),
            suggestions=[suggestion.content for suggestion in grade.suggestions] if grade.suggestions else [],
            user_input_code=grade.user_input_code.code if grade.user_input_code else None
        )
