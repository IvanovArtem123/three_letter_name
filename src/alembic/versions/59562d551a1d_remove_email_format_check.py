"""remove_email_format_check

Revision ID: 59562d551a1d
Revises: 8262560fb826
Create Date: 2026-06-05 19:54:06.996894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59562d551a1d'
down_revision: Union[str, Sequence[str], None] = '8262560fb826'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удаляем CHECK constraint
    op.drop_constraint('check_email_format', 'user', type_='check')

def downgrade():
    # Если нужно откатить - восстанавливаем
    op.create_check_constraint(
        'check_email_format', 
        'user', 
        "email IS NULL OR email ~ '^[^@]+@[^@]+\\.[^@]+$'"
    )
