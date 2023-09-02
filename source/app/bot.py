from telegram import error
from telegram.ext import Application
from app.settings import get_token, app_logger


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
