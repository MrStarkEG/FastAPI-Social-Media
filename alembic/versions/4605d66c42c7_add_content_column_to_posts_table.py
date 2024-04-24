"""add content column to posts table

Revision ID: 4605d66c42c7
Revises: 22b64fe2bbf9
Create Date: 2024-04-15 05:11:07.463620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4605d66c42c7'
down_revision: Union[str, None] = '22b64fe2bbf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
