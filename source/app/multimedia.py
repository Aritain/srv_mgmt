import os
import shutil

from .settings import get_multimedia_dir
from telegram.ext import (
    ConversationHandler
)


async def list_directories(update, context):
    dirs = os.listdir(get_multimedia_dir())
    reply_text = "Available multimedia directories:\n"
    for i, directory in enumerate(dirs):
        reply_text += f'({i+1}) {directory}\n'
    await update.message.reply_text(reply_text)
    return directory_choise


async def directory_choise(update, context):
    dirs = os.listdir(get_multimedia_dir())
    chosen_dir = dirs[int(update.message.text) - 1]
    shutil.rmtree(f'{get_multimedia_dir()}/{chosen_dir}')
    await update.message.reply_text('Done')
    return ConversationHandler.END
