from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import commands
from config import sys_dev
from lib.configlib import DefaultValues
from lib.logger import Logger

# handle config
_use_credentials = sys_dev
_use_namespace = sys_dev.kubernetes_config.namespace or DefaultValues.DEAFAULT_NAMESPACE


def main():
    application = ApplicationBuilder().token(_use_credentials.telegram_config.telegram_token).build()

    Logger.info("Connected to Telegram API successfully!")

    start_handler = CommandHandler('start', commands.start)
    fallback_handler = MessageHandler(filters.ALL, commands.main)

    application.add_handlers([start_handler, fallback_handler])

    application.run_polling()


if __name__ == '__main__':
    main()
