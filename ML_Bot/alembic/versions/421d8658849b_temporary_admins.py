"""temporary admins

Revision ID: 421d8658849b
Revises: a8a2108b7b78
Create Date: 2022-04-15 15:31:19.265211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '421d8658849b'
down_revision = 'a8a2108b7b78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp_admin',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('admin', sa.Column('username', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin', 'username')
    op.drop_table('temp_admin')
    # ### end Alembic commands ###
