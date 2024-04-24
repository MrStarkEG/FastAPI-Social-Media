"""Add last few columns to posts table

Revision ID: 1e881cee1644
Revises: fa177c7bb3cc
Create Date: 2024-04-21 13:48:23.893481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e881cee1644'
down_revision: Union[str, None] = 'fa177c7bb3cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(),
                  nullable=False, server_default=sa.text('NOW()')))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
