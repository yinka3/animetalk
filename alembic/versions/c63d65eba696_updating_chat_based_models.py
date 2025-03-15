"""updating chat-based models

Revision ID: c63d65eba696
Revises: 9e83deb26b54
Create Date: 2025-03-04 14:00:15.687312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c63d65eba696'
down_revision: Union[str, None] = '9e83deb26b54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

messagetype_enum = postgresql.ENUM('NEW_MESSAGE', 'EDITING', name='messagetype')

def upgrade() -> None:
    messagetype_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('messages', sa.Column('type', messagetype_enum, nullable=False))
    op.drop_column('messages', 'is_read')
    op.drop_column('messages', 'is_sender')



def downgrade() -> None:

    op.add_column('messages', sa.Column('is_sender', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('messages', sa.Column('is_read', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('messages', 'type')

    messagetype_enum.drop(op.get_bind(), checkfirst=True)
