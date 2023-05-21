from pprint import pprint

from telegram import Update
from telegram.ext import ContextTypes

from lib.db.db import Database
from lib.kubernetes.k8s import Kubernetes
from lib.kubernetes.objects import Namespace, Pod


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hi, 👋\nI am Skippo, your tech-savy chat bot with all of the integrated "
                                        "services and features!")


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # handle conversations here

    pass
