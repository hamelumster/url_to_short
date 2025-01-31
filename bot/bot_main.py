import os
from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from db.db_core import AsyncSessionLocal
from db.db_usage import DatabaseManager


token = os.getenv("TOKEN")

class Bot:
    def __init__(self, token: str):
        self.token = token
        self.app = ApplicationBuilder().token(self.token).build()
        self._register_handlers()
        self.session = AsyncSessionLocal

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    @asynccontextmanager
    async def with_db_session(self):
        session = self.session()
        try:
            yield DatabaseManager(session)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка в сессии БД: {e}")
            raise
        finally:
            await session.close()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            input_text = update.message.text
            user_id = update.message.from_user.id
            username = update.message.from_user.username or f"user_{user_id}"

            async with self.with_db_session() as db_manager:
                user = await db_manager.get_or_create_user(user_id, username)

                input_entry = await db_manager.save_input_text(user.id, input_text)
                output_entry = await db_manager.generate_short_url(input_entry)

            if output_entry:
                await update.message.reply_text(f"✅ Ваша короткая ссылка:\n\n{output_entry.short_url}")
            else:
                await update.message.reply_text("📝 Введенный текст не является ссылкой.\n"
                                                "Пожалуйста, пришли ссылку, которая начинается с http")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            await update.message.reply_text("⚠️ Произошла ошибка при обработке сообщения")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = update.message.from_user
            async with self.with_db_session() as db_manager:
                db_user = await db_manager.get_or_create_user(user.id, user.username or f"user_{user.id}")
            await update.message.reply_text("Привет! Я помогу сократить твои ссылки.\nПросто отправь мне URL.")
        except Exception as e:
            print(f"Ошибка в start: {str(e)}")
            await update.message.reply_text("⚠️ Ошибка сервера")

    # def run(self):
    #     self.app.run_polling()

    # Метод, который будет обрабатывать входящие Webhook-обновления
    async def process_update(self, update: dict):
        telegram_update = Update.de_json(update, self.app.bot)
        await self.app.process_update(telegram_update)
