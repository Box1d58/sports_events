"""Teams

Revision ID: 77a4b1012c81
Revises: 7b7815d95254
Create Date: 2025-02-28 00:40:57.708906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77a4b1012c81'
down_revision: Union[str, None] = '7b7815d95254'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('matches',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
    sa.Column('match_date', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('scores', sa.String(), nullable=False),
    sa.Column('owner', sa.Integer(), sa.ForeignKey('teams.id'), nullable=False),
    sa.Column('guest', sa.Integer(), sa.ForeignKey('teams.id'), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()'),
              nullable=False)
    )




def downgrade() -> None:
    op.execute('ALTER TABLE matches DROP CONSTRAINT IF EXISTS matches_owner_fkey')
    op.execute('ALTER TABLE matches DROP CONSTRAINT IF EXISTS matches_guest_fkey')

    op.execute('TRUNCATE TABLE matches RESTART IDENTITY CASCADE')
    op.drop_table('matches')
