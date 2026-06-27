"""integer-tg

Revision ID: f120cb387b09
Revises: 04d851ca268e
Create Date: 2026-06-05 01:45:48.712596

"""
from typing import Union, Sequence

from alembic import op
import sqlalchemy as sa


revision: str = 'f120cb387b09'
down_revision: Union[str, Sequence[str], None] = '04d851ca268e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Очищаем возможные пустые строки
    op.execute("UPDATE \"user\" SET tg_id = NULL WHERE tg_id = ''")
    
    # 2. Меняем тип с явным указанием USING
    op.execute('ALTER TABLE "user" ALTER COLUMN tg_id TYPE INTEGER USING tg_id::integer')
    
    # 3. Создаём индекс (опционально)
    op.create_index('ix_user_tg_id', 'user', ['tg_id'], unique=False)


def downgrade() -> None:
    # Удаляем индекс
    op.drop_index('ix_user_tg_id', table_name='user')
    
    # Возвращаем строковый тип
    op.execute('ALTER TABLE "user" ALTER COLUMN tg_id TYPE VARCHAR(64)')