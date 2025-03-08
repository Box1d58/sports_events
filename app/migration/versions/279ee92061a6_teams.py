"""Teams

Revision ID: 279ee92061a6
Revises:
Create Date: 2025-02-28 00:40:57.708906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '279ee92061a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('teams',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
    sa.Column('title', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('teams')
