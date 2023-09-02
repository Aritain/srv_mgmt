import asyncio
import shutil

from .bot import Bot
from .settings import get_bot_admin

def get_free_space() -> float:
    total, used, free = shutil.disk_usage('/')
    return free * 100 / total

async def report_disk(update, context) -> None:
    reply_text = f'{get_free_space()}%'
    output_free_space = "%.2f" % free_space
    await update.message.reply_text(reply_text)

def run_monitor_disk() -> None:
    asyncio.run(monitor_disk())

async def monitor_disk() -> None:
    bot = Bot()
    bot_admin = get_bot_admin()
    notification = True

    while True:
        free_space = get_free_space()
        output_free_space = "%.2f" % free_space
        if free_space < 25.0:
            if notification:
                notification = False
                reply_text = f'⚠️ Current free disk space is low - {output_free_space}%'
                await bot.send_message(chat_id = bot_admin, text = reply_text)
        else:
            notification = True

        await asyncio.sleep(5)
