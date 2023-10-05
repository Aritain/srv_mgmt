import asyncio

from telegram import error
from telegram.ext import Application
from app.settings import get_token, app_logger
from telegram.ext import ConversationHandler, ContextTypes

# Dedicated class so it's available within all app modules
class Bot:
    def __init__(self):
        self.application = Application.builder().token(get_token()).build()

    async def send_message(self, chat_id: int, text: str):
        try:
            app_logger.info(f'Attempting to send a message to {chat_id}')
            await self.application.bot.send_message(chat_id=chat_id, text=text)
        except (error.Forbidden, error.BadRequest):
            app_logger.warn(f'Failed to send messaage to {chat_id}')

    async def cancel_conversation(self, update, context):
        await update.message.reply_text('ok')
        return ConversationHandler.END

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        app_logger.error(f"Exception while handling an update: {context.error}")
        await asyncio.sleep(0)
        return ConversationHandler.END
