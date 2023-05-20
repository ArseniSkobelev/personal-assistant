from pprint import pprint

from telegram import Update
from telegram.ext import ContextTypes

from lib.db.db import Database
from lib.kubernetes.k8s import Kubernetes
from lib.kubernetes.objects import Namespace, Pod
from main import _use_credentials


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nginx_pod = Pod(pod_name='nginx', image='nginx')
    nginx_pod.delete_object(_use_credentials.kubernetes_config)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # handle conversations here

    pass

    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
