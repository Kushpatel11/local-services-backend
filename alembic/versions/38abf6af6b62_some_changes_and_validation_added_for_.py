"""some changes and validation added for ratings and status

Revision ID: 38abf6af6b62
Revises: 72384f58e89d
Create Date: 2025-06-07 11:43:17.271330

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "38abf6af6b62"
down_revision: Union[str, None] = "72384f58e89d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the ENUM type before altering the column
    booking_status_enum = sa.Enum(
        "pending",
        "approved",
        "rejected",
        "completed",
        "cancelled",
        name="bookingstatus",
    )
    booking_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "bookings",
        "status",
        existing_type=sa.VARCHAR(),
        type_=booking_status_enum,
        existing_nullable=False,
        postgresql_using="status::bookingstatus",
    )
    op.add_column(
        "service_categories", sa.Column("parent_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "service_categories", "service_categories", ["parent_id"], ["id"]
    )
    op.alter_column(
        "service_providers", "is_deleted", existing_type=sa.BOOLEAN(), nullable=False
    )
    op.add_column(
        "service_ratings", sa.Column("booking_id", sa.Integer(), nullable=False)
    )
    op.create_unique_constraint(None, "service_ratings", ["booking_id"])
    op.create_foreign_key(None, "service_ratings", "bookings", ["booking_id"], ["id"])
    op.add_column("services", sa.Column("min_price", sa.Float(), nullable=True))
    op.add_column("services", sa.Column("max_price", sa.Float(), nullable=True))
    op.drop_column("services", "price_range")
    op.alter_column("users", "is_deleted", existing_type=sa.BOOLEAN(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "is_deleted", existing_type=sa.BOOLEAN(), nullable=True)
    op.add_column(
        "services",
        sa.Column("price_range", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("services", "max_price")
    op.drop_column("services", "min_price")
    op.drop_constraint(None, "service_ratings", type_="foreignkey")
    op.drop_constraint(None, "service_ratings", type_="unique")
    op.drop_column("service_ratings", "booking_id")
    op.alter_column(
        "service_providers", "is_deleted", existing_type=sa.BOOLEAN(), nullable=True
    )
    op.drop_constraint(None, "service_categories", type_="foreignkey")
    op.drop_column("service_categories", "parent_id")
    op.alter_column(
        "bookings",
        "status",
        existing_type=sa.Enum(
            "pending",
            "approved",
            "rejected",
            "completed",
            "cancelled",
            name="bookingstatus",
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # Drop the ENUM type after reverting column
    booking_status_enum = sa.Enum(
        "pending",
        "approved",
        "rejected",
        "completed",
        "cancelled",
        name="bookingstatus",
    )
    booking_status_enum.drop(op.get_bind(), checkfirst=True)
