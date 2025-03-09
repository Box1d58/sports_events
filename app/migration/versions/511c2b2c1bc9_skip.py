"""Initial revision

Revision ID: 511c2b2c1bc9
Revises:
Create Date: 2024-11-05 15:48:58.628517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import foreign

from app.routes.teams_add import teams

revision: str = '511c2b2c1bc9'
down_revision: Union[str, None] = '77a4b1012c81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass



def downgrade() -> None:
    pass
