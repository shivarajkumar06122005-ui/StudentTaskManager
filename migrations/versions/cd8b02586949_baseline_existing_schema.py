"""baseline existing schema

Revision ID: cd8b02586949
Revises:
Create Date: 2026-11-26 20:00:15.656525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd8b02586949'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline only: existing production schema is already in place."""
    pass


def downgrade() -> None:
    """No schema changes to reverse for this baseline."""
    pass
