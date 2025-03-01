"""init migration

Revision ID: 83b6d23c3274
Revises:
Create Date: 2025-03-01 02:02:23.583594

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83b6d23c3274"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # companies
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # company_localized_names
    op.create_table(
        "company_localized_names",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Index(
            "ix_company_localized_names_company_id_language", "company_id", "language"
        ),
        sa.Index("ix_company_localized_names_name", "name"),
    )

    op.create_foreign_key(
        "fk_company_localized_names_company_id",
        "company_localized_names",
        "companies",
        ["company_id"],
        ["id"],
    )

    op.create_unique_constraint(
        "unique_company_localized_name_company_id_name_language",
        "company_localized_names",
        ["company_id", "name", "language"],
    )

    # company_name_tokens 테이블 생성
    op.create_table(
        "company_name_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id"),
            nullable=False,
        ),
        sa.Column("tokenized_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_company_name_tokens_tokenized_name", "tokenized_name"),
    )

    op.create_foreign_key(
        "fk_company_name_tokens_company_id",
        "company_name_tokens",
        "companies",
        ["company_id"],
        ["id"],
    )

    # company_tags
    op.create_table(
        "company_tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id"),
            nullable=False,
        ),
        sa.Column("tag", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_company_tags_tag", "tag"),
    )

    op.create_foreign_key(
        "fk_company_tags_company_id",
        "company_tags",
        "companies",
        ["company_id"],
        ["id"],
    )

    op.create_unique_constraint(
        "unique_company_tags_company_id_tag_language",
        "company_tags",
        ["company_id", "tag", "language"],
    )


def downgrade():
    op.drop_table("company_name_tokens")
    op.drop_table("company_localized_names")
    op.drop_table("company_tags")
    op.drop_table("companies")
