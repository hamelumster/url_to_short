import os
import asyncio

from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler

token = os.getenv("TOKEN")


class Bot:
    def __init__(self, token: str):
        self.token = token
        self.app = ApplicationBuilder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello! I'm working")

    def run(self):
        self.app.run_polling()