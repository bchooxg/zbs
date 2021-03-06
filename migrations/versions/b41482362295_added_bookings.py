"""added bookings

Revision ID: b41482362295
Revises: 43059a6e7ce4
Create Date: 2020-11-01 07:43:31.272665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41482362295'
down_revision = '43059a6e7ce4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.create_foreign_key(None, 'booking', 'slot', ['slot_id'], ['id'])
    op.create_foreign_key(None, 'booking', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.create_foreign_key(None, 'booking', 'channel', ['slot_id'], ['id'])
    op.create_foreign_key(None, 'booking', 'channel', ['user_id'], ['id'])
    # ### end Alembic commands ###
