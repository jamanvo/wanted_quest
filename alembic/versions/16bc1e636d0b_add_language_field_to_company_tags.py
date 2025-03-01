"""add language field to company_tags

Revision ID: 16bc1e636d0b
Revises: 83b6d23c3274
Create Date: 2025-03-01 16:19:13.084342

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16bc1e636d0b"
down_revision: Union[str, None] = "83b6d23c3274"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("company_tags", sa.Column("language", sa.String(), nullable=False))

    op.create_unique_constraint(
        "unique_company_tags_company_id_tag_language",
        "company_tags",
        ["company_id", "tag", "language"],
    )


def downgrade() -> None:
    op.drop_column("company_tags", "language")
