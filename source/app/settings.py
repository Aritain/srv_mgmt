import logging
import os
import sys

CANCEL_CAPTION = "no"

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
app_logger = logging.getLogger('app_logger')

def get_token() -> str:
    try:
        token = os.environ['TG_TOKEN']
    except KeyError:
        app_logger.error('Missing TG_TOKEN env varbiable')
        sys.exit(1)
    return token


def get_bot_admin() -> int:
    try:
        admin_id = int(os.environ['BOT_ADMIN'])
    except (KeyError, ValueError):
        app_logger.error('Missing BOT_ADMIN env varbiable')
        sys.exit(1)
    return admin_id


def get_multimedia_dir() -> str:
    try:
        multimedia_dir = os.environ['MULTIMEDIA_DIR']
    except (KeyError, ValueError):
        app_logger.error('Missing MULTIMEDIA_DIR env varbiable')
        sys.exit(1)
    return multimedia_dir
