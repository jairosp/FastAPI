"""add foreign key to post table

Revision ID: e44ddb17abed
Revises: ef083da6e34b
Create Date: 2025-01-12 13:25:14.948012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e44ddb17abed'
down_revision: Union[str, None] = 'ef083da6e34b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 
                          source_table='posts', 
                          referent_table='users', 
                          local_cols=['owner_id'], 
                          remote_cols=['id'], 
                          ondelete="CASCADE"
                        )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
