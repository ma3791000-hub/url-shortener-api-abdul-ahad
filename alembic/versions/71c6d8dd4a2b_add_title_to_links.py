"""add title to links

Revision ID: 71c6d8dd4a2b
Revises: b1eede26f2b5
Create Date: 2026-11-03 16:23:31.514892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
revision: str = '71c6d8dd4a2b'
down_revision: Union[str, Sequence[str], None] = 'b1eede26f2b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('links', sa.Column('title', sa.String(length=255), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('links', 'title')
    
