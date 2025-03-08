"""Users

Revision ID: 7b7815d95254
Revises: 279ee92061a6
Create Date: 2025-02-27 18:19:45.849905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7b7815d95254'
down_revision: Union[str, None] = '279ee92061a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('user id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('nickname', sa.String(), nullable=False),
    sa.Column('follow_team', sa.Integer(), sa.ForeignKey('teams.id')),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
   op.drop_table('users')
