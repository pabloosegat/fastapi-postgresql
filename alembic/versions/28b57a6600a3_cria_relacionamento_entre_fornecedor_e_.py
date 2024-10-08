"""Cria relacionamento entre fornecedor e conta

Revision ID: 28b57a6600a3
Revises: 658866251765
Create Date: 2024-09-16 15:14:35.718355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b57a6600a3'
down_revision = '658866251765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_contas', sa.Column('id_fornecedor_cliente', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tbl_contas', 'tbl_fornecedor_cliente', ['id_fornecedor_cliente'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tbl_contas', type_='foreignkey')
    op.drop_column('tbl_contas', 'id_fornecedor_cliente')
    # ### end Alembic commands ###
