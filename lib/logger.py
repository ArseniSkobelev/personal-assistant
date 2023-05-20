from datetime import datetime
from lib.text_formatting import Colors, Styles
from config import (
    BOT_NAME,
    LOG_CONNECTOR,
)


class Logger:
    @staticmethod
    def info(message):
        print(
            Colors.INFO + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.INFO + Styles.BOLD + f"{BOT_NAME}{LOG_CONNECTOR}" + Colors.NC + Colors.INFO + f"{message}" + Colors.NC)

    @staticmethod
    def error(message):
        print(
            Colors.ERROR + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.ERROR + Styles.BOLD + f"{BOT_NAME}{LOG_CONNECTOR}" + Colors.NC + Colors.ERROR + f"{message}" + Colors.NC)

    @staticmethod
    def attention(message):
        print(
            Colors.ATTENTION + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.ATTENTION + Styles.BOLD + f"{BOT_NAME}{LOG_CONNECTOR}" + Colors.NC + Colors.ATTENTION + f"{message}" + Colors.NC)

    @staticmethod
    def success(message):
        print(
            Colors.SUCCESS + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.SUCCESS + Styles.BOLD + f"{BOT_NAME}{LOG_CONNECTOR}" + Colors.NC + Colors.SUCCESS + f"{message}" + Colors.NC)
