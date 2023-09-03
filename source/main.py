import asyncio
import threading

from app.settings import (
    app_logger,
    CANCEL_CAPTION,
    get_bot_admin
)
from telegram.ext import (
    CommandHandler, MessageHandler, filters,
    ConversationHandler
) 
from app.disk import (
    report_disk,
    run_monitor_disk
)
from app.bot import (
    Bot
)
from app.docker import (
    ContainerHandler
)


def main():
    bot_admin = get_bot_admin()
    app_logger.info('Starting Bot & Polling...')
    disk_mon = threading.Thread(target=run_monitor_disk)
    disk_mon.start()

    bot = Bot()
    container_handler = ContainerHandler()
    
    bot.application.add_handler(CommandHandler("disk", report_disk, filters.User(bot_admin)))
    bot.application.add_handler(ConversationHandler(
        entry_points = [CommandHandler("docker", container_handler.container_list)],
        states = {
            container_handler.container_logs : [
                MessageHandler(
                    filters.TEXT & ~filters.Regex(CANCEL_CAPTION), container_handler.container_logs
                )
            ]
        },
        fallbacks=[
            MessageHandler(
                filters.Regex(CANCEL_CAPTION), container_handler.container_cancel
            )]
    ))
    '''
    bot.application.add_handler(ConversationHandler(
        entry_points = [CommandHandler("multimedia", multimedia, filters.User(bot_admin))],
        states = {
            multimedia_pick : [
                MessageHandler(
                    filters.TEXT & ~filters.Regex(CANCEL_CAPTION), multimedia_pick
                )
            ]
        }
    ))
    '''

    bot.application.run_polling()

if __name__ == "__main__":
    main()
