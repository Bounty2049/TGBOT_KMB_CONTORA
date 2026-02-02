import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
import aiosqlite 
from dotenv import load_dotenv
import os
from datetime import date, time, datetime, timedelta
import pytz

from main import get_random_term

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

async def add_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        """)
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, last_name))
        await db.commit()

@dp.message(Command("term"))
async def cmd_term(message: Message):
    record = get_random_term()
    term_message = str()
    for r in record:
        term_message = f"{r[1]} - {r[2]}"
    await message.answer(
        term_message,
        parse_mode=ParseMode.HTML
    )

async def get_all_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows] # Список ID пользователей 

# Отправит рандомный термин раз в некоторое время всем пользователям из базы данных 
async def scheduled_message():
    while True:
        now = datetime.now(pytz.timezone("Asia/Yekaterinburg"))
        current_time = now.time()

        # if time(8, 0) <= current_time <= time(23, 59, 59):
        record = get_random_term()
        term_message = str()
        for r in record:
            term_message = f"{r[1]} - {r[2]}"

        users = await get_all_users()  
        for user_id in users:
            try:
                await bot.send_message(user_id, term_message, parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.error(f"Failed to send message to {user_id}: {e}")

        await asyncio.sleep(10)  # Ждать 3 минуты перед следующим сообщением (3600 секунд = 1 час)

async def main():
    logger.info("Starting bot")
    await asyncio.gather(
        dp.start_polling(bot),
        scheduled_message()
    )


if __name__ == "__main__":
    asyncio.run(main())