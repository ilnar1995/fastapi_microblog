"""fixed column date in user model

Revision ID: a4910cfc67f9
Revises: 6c066d0a22ea
Create Date: 2023-06-05 16:48:37.517230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4910cfc67f9'
down_revision = '6c066d0a22ea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_microblog_posts_date'), 'microblog_posts', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_microblog_posts_date'), table_name='microblog_posts')
    # ### end Alembic commands ###
