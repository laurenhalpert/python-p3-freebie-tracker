"""add Freebie

Revision ID: a32e60ac241e
Revises: 5f72c58bf48c
Create Date: 2023-05-11 11:20:04.968121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a32e60ac241e'
down_revision = '5f72c58bf48c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('freebies')


def downgrade() -> None:
    op.drop_table('freebies')
