import asyncio

from bot.bot_main import Bot
import os
from dotenv import load_dotenv

from db.db_core import create_tables

load_dotenv()

if __name__ == '__main__':
    token = os.getenv("TOKEN")
    print('Bot started!')
    bot = Bot(token)
    asyncio.run(create_tables())
    # bot.run()