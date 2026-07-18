Saul Goodman VPN

VPN-сервис 3x-ui + FastAPI + Telegram Bot

Запуск проекта:
1) git clone https://github.com/IvanovArtem123/Saul_Goodman_VPN.git
2) В корне проекта создаём виртуальное окружение: python3.14 -m venv venv (для винды py -3.14 -m venv venv)
3) Активация виртуального окружения: source venv/bin/activate
4) Устанавливаем зависимости: pip install -r requirements.txt
5) Поднимаем Dokcer с базой данных: docker compose up -d
6) Применяем миграции: alembic upgrade head
7) Запуск:
   1. Переходим в директорию с бэком: сd src
   2. Запускаем FastAPI приложение: python main.py
