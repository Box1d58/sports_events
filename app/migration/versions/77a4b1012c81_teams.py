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
