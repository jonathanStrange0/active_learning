"""added a single bin for flashcards

Revision ID: c3d599eb853f
Revises: 9bccb577ad2e
Create Date: 2019-07-11 05:20:21.812987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d599eb853f'
down_revision = '9bccb577ad2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bin_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bin_bin_name'), 'bin', ['bin_name'], unique=True)
    op.add_column('note', sa.Column('bin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'note', 'bin', ['bin_id'], ['id'])
    op.add_column('quiz', sa.Column('learning_session_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'quiz', 'learning_session', ['learning_session_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quiz', type_='foreignkey')
    op.drop_column('quiz', 'learning_session_id')
    op.drop_constraint(None, 'note', type_='foreignkey')
    op.drop_column('note', 'bin_id')
    op.drop_index(op.f('ix_bin_bin_name'), table_name='bin')
    op.drop_table('bin')
    # ### end Alembic commands ###