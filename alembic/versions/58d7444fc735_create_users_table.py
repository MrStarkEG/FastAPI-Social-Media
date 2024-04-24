"""Create users table

Revision ID: 58d7444fc735
Revises: 4605d66c42c7
Create Date: 2024-04-15 05:23:36.659873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58d7444fc735'
down_revision: Union[str, None] = '4605d66c42c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),  # make it the primary key
                    # another way --> primary_key=True
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
