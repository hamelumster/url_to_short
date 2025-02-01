import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import RedirectResponse

from bot.bot_main import Bot
from db.db_core import create_tables, AsyncSessionLocal
from db.db_usage import DatabaseManager

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

@app.get("/{short_code}")
async def redirect_short_url(short_code: str):
    # Функция для поиска оригинальной ссылки по коду в БД
    async with AsyncSessionLocal() as session:
        db_manager = DatabaseManager(session)
        original_url = await db_manager.get_original_url(short_code)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
