"""rename student_id to member_id and add is_creator

Revision ID: 351d631c018b
Revises: 9ba6d912d517
Create Date: 2026-03-19 13:26:24.376589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '351d631c018b'
down_revision = '9ba6d912d517'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('classroom_members', schema=None) as batch_op:

        # ➕ add member_id (nullable first to avoid crash)
        batch_op.add_column(sa.Column('member_id', sa.Integer(), nullable=True))

        # ➕ add is_creator with default False
        batch_op.add_column(
            sa.Column(
                'is_creator',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()   # 🔥 important
            )
        )

        # 🔗 drop old FK
        batch_op.drop_constraint('classroom_members_ibfk_2', type_='foreignkey')

        # ❌ drop old column
        batch_op.drop_column('student_id')

        # 🔗 create new FK
        batch_op.create_foreign_key(
            'fk_classroom_members_member_id_users',
            'users',
            ['member_id'],
            ['Uid']
        )

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('classroom_members', schema=None) as batch_op:

        # 🔙 bring back student_id
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=True))

        # 🔗 restore FK
        batch_op.create_foreign_key(
            'classroom_members_ibfk_2',
            'users',
            ['student_id'],
            ['Uid']
        )

        # ❌ drop new FK
        batch_op.drop_constraint('fk_classroom_members_member_id_users', type_='foreignkey')

        # ❌ drop new columns
        batch_op.drop_column('member_id')
        batch_op.drop_column('is_creator')
