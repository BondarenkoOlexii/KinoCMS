import psycopg2
import sys

# Впишіть сюди ваші дані точно як в settings.py
DB_NAME = "kinocms"  # Перевірте назву!
USER = "kinocms_admin"
PASSWORD = "1234" # <--- Впишіть пароль
HOST = "127.0.0.1"
PORT = "5432"        # Або 5433, якщо в Shell було так

print(f"--- Спроба підключення до {DB_NAME} на {HOST}:{PORT} ---")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    print("✅ УСПІХ! База доступна, логін/пароль вірні.")
    conn.close()
except Exception as e:
    print("\n❌ ПОМИЛКА ПІДКЛЮЧЕННЯ:")
    print(e)