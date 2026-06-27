from datetime import datetime
from constants import FORMAT_END_DATE


async def get_current_datetime(backend_datetime: str) -> str:
    '''Переводит время с бэкенда в читаемое.'''
    dt_end_date = datetime.fromisoformat(backend_datetime.replace(
        'Z', '+00:00')).strftime(FORMAT_END_DATE)
    return dt_end_date
