import os
from datetime import datetime
from lib.text_formatting import Colors, Styles


class Logger:
    @staticmethod
    def info(message):
        print(
            Colors.INFO + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS +
            Colors.INFO + Styles.BOLD + f"{os.getenv('HUB_BOT_NAME')}{os.getenv('HUB_LOG_CONNECTOR')}" + Colors.NC + Colors.INFO + f"{message}" +
            Colors.NC)

    @staticmethod
    def error(message):
        print(
            Colors.ERROR + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.ERROR + Styles.BOLD + f"{os.getenv('HUB_BOT_NAME')}{os.getenv('HUB_LOG_CONNECTOR')}" + Colors.NC + Colors.ERROR + f"{message}" + Colors.NC)

    @staticmethod
    def attention(message):
        print(
            Colors.ATTENTION + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.ATTENTION + Styles.BOLD + f"{os.getenv('HUB_BOT_NAME')}{os.getenv('HUB_LOG_CONNECTOR')}" + Colors.NC + Colors.ATTENTION + f"{message}" + Colors.NC)

    @staticmethod
    def success(message):
        print(
            Colors.SUCCESS + Styles.ITALIC + f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ' + Styles.NS + Colors.SUCCESS + Styles.BOLD + f"{os.getenv('HUB_BOT_NAME')}{os.getenv('HUB_LOG_CONNECTOR')}" + Colors.NC + Colors.SUCCESS + f"{message}" + Colors.NC)
