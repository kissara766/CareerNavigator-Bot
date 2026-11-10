import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Токен бота берём из .env (переменная BOT_TOKEN).
# Сам токен в коде не храним — он лежит только в .env.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Название файла базы данных
DB_NAME = "database.db"
