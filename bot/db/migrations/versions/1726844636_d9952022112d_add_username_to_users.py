"""Add username to users.

Revision ID: d9952022112d
Revises: b4f9746b888d
Create Date: 2024-09-20 15:03:56.329135+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d9952022112d"
down_revision: str | None = "b4f9746b888d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("username", sa.String(), nullable=True))
        batch_op.create_unique_constraint(op.f("uq_users_username"), ["username"])


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(op.f("uq_users_username"), type_="unique")
        batch_op.drop_column("username")
