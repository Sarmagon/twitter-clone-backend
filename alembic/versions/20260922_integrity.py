"""Deduplicate relationships, constrain pairs, and track upload ownership.

Existing duplicate rows describe the same relationship; keep the oldest ID.
The pre-upgrade database dump is required to recover removed duplicate rows.
"""

import sqlalchemy as sa

from alembic import op

revision = "20260922_integrity"
down_revision = "2f4d31d9d0d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Preserve each logical relationship and add uniqueness."""
    for table, a, b in [
        ("likes", "user_id", "tweet_id"),
        ("follows", "follower_id", "following_id"),
    ]:
        op.execute(
            sa.text(
                f"DELETE FROM {table} WHERE id NOT IN (SELECT MIN(id) FROM {table} GROUP BY {a}, {b})"
            )
        )
        op.create_unique_constraint(f"uq_{table}_pair", table, [a, b])
    op.add_column("medias", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_medias_owner", "medias", "users", ["owner_id"], ["id"], ondelete="SET NULL"
    )
    op.execute(
        sa.text(
            "UPDATE medias SET owner_id = tweets.author_id FROM tweets WHERE medias.tweet_id = tweets.id"
        )
    )


def downgrade() -> None:
    """Remove new constraints; duplicate rows cannot be reconstructed here."""
    op.drop_constraint("fk_medias_owner", "medias", type_="foreignkey")
    op.drop_column("medias", "owner_id")
    op.drop_constraint("uq_follows_pair", "follows", type_="unique")
    op.drop_constraint("uq_likes_pair", "likes", type_="unique")
