"""add Rooms table

Revision ID: 74813af7a3c3
Revises: 7dd2fc23dbbb
Create Date: 2025-02-03 15:30:07.047448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '74813af7a3c3'
down_revision: Union[str, None] = '7dd2fc23dbbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('hotel_id', sa.Integer, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('price', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKey('hotels.id'),
    )


def downgrade() -> None:
    op.drop_table('rooms')
