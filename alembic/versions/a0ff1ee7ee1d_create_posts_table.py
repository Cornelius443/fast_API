"""create posts table

Revision ID: a0ff1ee7ee1d
Revises: 
Create Date: 2025-02-17 16:23:27.625599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0ff1ee7ee1d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String(50), nullable=False),
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
