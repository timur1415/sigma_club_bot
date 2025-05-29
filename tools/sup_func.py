import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from config.config import TGK_ID

async def is_channel_subscribed(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    member = await context.bot.get_chat_member(TGK_ID, user_id)
    print(member.status)
    if member.status in ['member', 'creator', 'administrator']:
        return True
    else:
        return False
    