"""Add event_count to users.

Revision ID: 3589074a9b3b
Revises: d9952022112d
Create Date: 2024-10-16 13:36:33.164782+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3589074a9b3b"
down_revision: str | None = "d9952022112d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("event_count", sa.BigInteger(), server_default=sa.text("0"), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "event_count")
