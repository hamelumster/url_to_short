from bot.bot_main import Bot
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    token = os.getenv("TOKEN")
    print('Bot started!')
    bot = Bot(token)
    # bot.run()