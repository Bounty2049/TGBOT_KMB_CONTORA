import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
import aiosqlite 
from dotenv import load_dotenv
import os
from datetime import time, datetime
import pytz

from cruddb import get_random_term, get_all_users, add_user

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

async def get_record():
    record = await get_random_term()
    term_message = str()
    for r in record:
        term_message = f"{r[1]} - {r[2]}"

    return term_message


@dp.message(Command("term"))
async def cmd_term(message: Message):
    await message.answer(
        await get_record(),
        parse_mode=ParseMode.HTML
    )

# Отправит рандомный термин раз в некоторое время всем пользователям из базы данных 
async def scheduled_message():
    while True:
        now = datetime.now(pytz.timezone("Asia/Yekaterinburg"))
        current_time = now.time()

        if time(8, 0) <= current_time <= time(23, 59, 59):
            users = await get_all_users()  
            for user_id in users:
                try:
                    await bot.send_message(user_id, await get_record(), parse_mode=ParseMode.HTML)
                except Exception as e:
                    logger.error(f"Failed to send message to {user_id}: {e}")

        await asyncio.sleep(5400)  # Ждать 1.5 часа перед следующим сообщением (3600 секунд = 1 час)


async def main():
    logger.info("Starting bot")
    await asyncio.gather(
        dp.start_polling(bot),
        scheduled_message()
    )


if __name__ == "__main__":
    asyncio.run(main())