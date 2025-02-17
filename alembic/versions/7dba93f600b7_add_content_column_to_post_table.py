"""add content column to post table

Revision ID: 7dba93f600b7
Revises: a0ff1ee7ee1d
Create Date: 2025-02-17 17:01:42.562437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dba93f600b7'
down_revision: Union[str, None] = 'a0ff1ee7ee1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
