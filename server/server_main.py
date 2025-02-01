import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from bot.bot_main import Bot
from db.db_core import create_tables

# Загружаем переменные из .env
load_dotenv()
token = os.getenv("TOKEN")

# Создаем бота
bot = Bot(token)

# Инициализируем FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Инициализируем приложения бота
    await bot.app.initialize()
    # Создаем таблицы в БД
    await create_tables()

@app.get("/")
async def home():
    return {"message": "Bot is running!"}

@app.post("/")
async def recieve_update(request: Request):
    """Process input Webhook-requests from Telegram"""
    update = await request.json()
    await bot.process_update(update)
    return {"ok": True}


