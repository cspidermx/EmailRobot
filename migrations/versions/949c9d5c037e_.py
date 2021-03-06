"""empty message

Revision ID: 949c9d5c037e
Revises: fb24ce02033a
Create Date: 2018-05-10 15:40:10.361988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '949c9d5c037e'
down_revision = 'fb24ce02033a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alerta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alert_details', sa.String(), nullable=True),
    sa.Column('start_datetime', sa.DateTime(), nullable=True),
    sa.Column('end_datetime', sa.DateTime(), nullable=True),
    sa.Column('managed_object', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('rating', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('analysis_tools', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asunto', sa.String(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('cliente', sa.String(), nullable=True),
    sa.Column('idmsg', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email_from',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email_to',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('to', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_to')
    op.drop_table('email_from')
    op.drop_table('email')
    op.drop_table('alerta')
    # ### end Alembic commands ###
