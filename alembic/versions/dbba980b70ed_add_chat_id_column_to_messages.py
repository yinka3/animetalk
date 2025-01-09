"""Add chat_id column to messages

Revision ID: dbba980b70ed
Revises: 
Create Date: 2024-12-30 21:07:55.832641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbba980b70ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
    # ### end Alembic commands ###
