"""init tables

Revision ID: 1183e829469e
Revises: 
Create Date: 2024-07-18 18:17:53.345743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1183e829469e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('language', sa.String(length=50), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('create_date'),
    sa.UniqueConstraint('email')
    )
    op.create_table('quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_language', sa.String(length=50), nullable=False),
    sa.Column('target_language', sa.String(length=50), nullable=False),
    sa.Column('difficulty', sa.String(length=50), nullable=False),
    sa.Column('category_type', sa.String(length=50), nullable=False),
    sa.Column('category_detail', sa.String(length=100), nullable=False),
    sa.Column('quiz', sa.Text(), nullable=False),
    sa.Column('hint_source_language_code', sa.Text(), nullable=False),
    sa.Column('hint_description', sa.Text(), nullable=False),
    sa.Column('answer_code', sa.Text(), nullable=False),
    sa.Column('user_email', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['user_email'], ['profile.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_score', sa.Integer(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('positive_feedback', sa.Text(), nullable=True),
    sa.Column('best_practice_code', sa.Text(), nullable=True),
    sa.Column('best_practice_explanation', sa.Text(), nullable=True),
    sa.Column('source_language', sa.String(length=50), nullable=True),
    sa.Column('target_language', sa.String(length=50), nullable=True),
    sa.Column('difficulty', sa.String(length=50), nullable=True),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('user_email', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['user_email'], ['profile.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accuracy', sa.Text(), nullable=True),
    sa.Column('efficiency', sa.Text(), nullable=True),
    sa.Column('readability', sa.Text(), nullable=True),
    sa.Column('pep8_compliance', sa.Text(), nullable=True),
    sa.Column('modularity_reusability', sa.Text(), nullable=True),
    sa.Column('exception_handling', sa.Text(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('score_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accuracy', sa.Integer(), nullable=True),
    sa.Column('efficiency', sa.Integer(), nullable=True),
    sa.Column('readability', sa.Integer(), nullable=True),
    sa.Column('pep8_compliance', sa.Integer(), nullable=True),
    sa.Column('modularity_reusability', sa.Integer(), nullable=True),
    sa.Column('exception_handling', sa.Integer(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('suggestions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_input_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_input_codes')
    op.drop_table('suggestions')
    op.drop_table('score_details')
    op.drop_table('feedback_details')
    op.drop_table('grade')
    op.drop_table('quiz')
    op.drop_table('profile')
    # ### end Alembic commands ###
