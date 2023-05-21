import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import commands
from lib.kubernetes.objects import Pod
from lib.logger import Logger

# handle config
try:
    load_dotenv(dotenv_path=".env")
except Exception as e:
    raise e


def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_API_TOKEN")).build()

    Logger.info("Connected to Telegram API successfully!")

    start_handler = CommandHandler('start', commands.start)
    fallback_handler = MessageHandler(filters.ALL, commands.main)

    application.add_handlers([start_handler, fallback_handler])

    application.run_polling()


if __name__ == '__main__':
    main()
