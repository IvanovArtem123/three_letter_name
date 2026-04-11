from dotenv import set_key, find_dotenv


async def add_dotenv(key: str, value: str) -> None:
    try:
        env_path = find_dotenv()
        set_key(env_path, key, value)
    except Exception as e:
        print(f"Ошибка при добавлении переменной {key}: {e}")
