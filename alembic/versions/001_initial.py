"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "identities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("organization_id", sa.String(64), nullable=True),
        sa.Column("public_key", sa.Text, nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False, unique=True),
        sa.Column("role", sa.String(50), server_default="analyst"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("last_seen", sa.DateTime, nullable=True),
    )

    op.create_table(
        "campaigns",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("severity", sa.String(20), server_default="medium"),
        sa.Column("confidence", sa.String(20), server_default="medium"),
        sa.Column("actor", sa.String(200), nullable=True),
        sa.Column("motivation", sa.String(500), nullable=True),
        sa.Column("target_sectors", sa.JSON, server_default="[]"),
        sa.Column("target_regions", sa.JSON, server_default="[]"),
        sa.Column("tags", sa.JSON, server_default="[]"),
        sa.Column("report_ids", sa.JSON, server_default="[]"),
        sa.Column("version", sa.Integer, server_default="1"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "threat_reports",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("threat_type", sa.String(50), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("confidence", sa.String(20), server_default="medium"),
        sa.Column("tlp_level", sa.String(20), server_default="green"),
        sa.Column("satellite_intrusion_type", sa.String(50), nullable=True),
        sa.Column("gnss_types", sa.JSON, server_default="[]"),
        sa.Column("affected_satellites", sa.JSON, server_default="[]"),
        sa.Column("affected_systems", sa.JSON, server_default="[]"),
        sa.Column("start_time", sa.DateTime, nullable=True),
        sa.Column("end_time", sa.DateTime, nullable=True),
        sa.Column("observables", sa.JSON, server_default="[]"),
        sa.Column("courses_of_action", sa.JSON, server_default="[]"),
        sa.Column("tags", sa.JSON, server_default="[]"),
        sa.Column("references", sa.JSON, server_default="[]"),
        sa.Column("author_id", sa.String(64), sa.ForeignKey("identities.id"), nullable=False),
        sa.Column("organization_id", sa.String(64), nullable=True),
        sa.Column("signature", sa.Text, nullable=True),
        sa.Column("signature_verified", sa.Boolean, server_default="false"),
        sa.Column("version", sa.Integer, server_default="1"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index("ix_threat_reports_type", "threat_reports", ["threat_type"])
    op.create_index("ix_threat_reports_severity", "threat_reports", ["severity"])
    op.create_index("ix_threat_reports_created", "threat_reports", ["created_at"])
    op.create_index("ix_threat_reports_author", "threat_reports", ["author_id"])


def downgrade() -> None:
    op.drop_table("threat_reports")
    op.drop_table("campaigns")
    op.drop_table("identities")
