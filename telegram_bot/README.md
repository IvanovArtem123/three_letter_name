# Telegram Bot для SoulGoodman VPN

Telegram бот для управления VPN подписками через API.

## Возможности

### Для пользователей:
- `/start` - Начать работу с ботом
- `/help` - Список команд
- `/my_subs` - Просмотр своих подписок
- `/sub_info <код>` - Информация о подписке и ключи доступа
- `/panels` - Список доступных VPN панелей

### Для администраторов:
- `/users` - Список всех пользователей
- `/all_subs` - Статистика по всем подпискам
- `/create_sub` - Создать новую подписку для пользователя

## Установка

1. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен

2. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

3. Заполните `.env`:
```env
BOT_TOKEN=your_bot_token_from_botfather
API_BASE_URL=http://backend:8000
ADMIN_IDS=123456789,987654321
```

4. Добавьте сервис в docker-compose.yml:
```yaml
telegram_bot:
  build: ./telegram_bot
  env_file:
    - ./telegram_bot/.env
  depends_on:
    - backend
  networks:
    - app_network
  restart: unless-stopped
```

5. Запустите:
```bash
docker-compose up -d telegram_bot
```

## Структура проекта

```
telegram_bot/
├── bot.py              # Главный файл запуска
├── handlers.py         # Обработчики команд
├── api_client.py       # Клиент для работы с API
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости Python
├── Dockerfile          # Docker образ
└── .env               # Переменные окружения (не коммитить!)
```

## Разработка

Для локальной разработки:

```bash
cd telegram_bot
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
python bot.py
```

## API Endpoints

Бот использует следующие эндпоинты бэкенда:

- `GET /api/users/{user_id}` - Информация о пользователе
- `GET /api/users/get_all` - Все пользователи
- `PATCH /api/users/update/{user_id}` - Обновление пользователя
- `POST /api/sub/create` - Создание подписки
- `GET /api/sub/get_all` - Все подписки
- `GET /api/sub/{sub_code}` - Информация о подписке
- `GET /api/panels/get_all` - Все панели
