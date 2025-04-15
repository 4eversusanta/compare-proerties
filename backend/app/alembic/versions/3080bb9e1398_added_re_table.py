"""Added re tables

Revision ID: 3080bb9e1398
Revises: 1a31ce608336
Create Date: 2025-04-09 21:03:55.911407

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlmodel.sql.sqltypes import AutoString


# revision identifiers, used by Alembic.
revision = '3080bb9e1398'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None



def upgrade():
    # Developer Table
    op.create_table(
        'developer',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', AutoString(length=128), nullable=False, index=True),
        sa.Column('reputation', AutoString(length=256), nullable=True),
        sa.Column('additional_info', sa.Text, nullable=True)
    )
    # Project Table
    op.create_table(
        'project',
         sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', AutoString(length=128), nullable=False, index=True),
        sa.Column('location', AutoString(length=128), nullable=True),
        sa.Column('latitude', sa.Float, nullable=True, index=True),
        sa.Column('longitude', sa.Float, nullable=True, index=True),
        sa.Column('pricing_range', AutoString(length=64), nullable=True),
        sa.Column('possession_date', AutoString(length=64), nullable=True),
        sa.Column('project_type', AutoString(length=128), nullable=True),
        sa.Column('website', AutoString(length=256), nullable=True),
        sa.Column('reraId', AutoString(length=128), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('area', sa.Text, nullable=True),
        sa.Column('image_url',AutoString(length=256), nullable=True),
        sa.Column('key_amenities', sa.Text, nullable=True),
        sa.Column('developer_id', sa.UUID(as_uuid=True), sa.ForeignKey('developer.id', ondelete="CASCADE"), nullable=False, index=True)
    )

    # SWOT Table
    op.create_table(
        'swot',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('category', AutoString(length=32), nullable=False, index=True), # E.g., Strength, Weakness
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('project_id', sa.UUID(as_uuid=True), sa.ForeignKey('project.id', ondelete="CASCADE"), nullable=False, index=True)

    )

    # Optional: amenity Table
    op.create_table(
        'amenity',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', sa.UUID(as_uuid=True), sa.ForeignKey('project.id', ondelete="CASCADE"), nullable=False),
        sa.Column('amenity_name', AutoString(length=128), nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=True)
    )


def downgrade():
    op.drop_table('amenity')
    op.drop_table('swot')
    op.drop_table('project')
    op.drop_table('developer')
