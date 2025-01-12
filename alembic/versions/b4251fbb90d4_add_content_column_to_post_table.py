"""add content column to post table

Revision ID: b4251fbb90d4
Revises: a61e06d59a65
Create Date: 2025-01-12 13:12:16.643380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4251fbb90d4'
down_revision: Union[str, None] = 'a61e06d59a65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
