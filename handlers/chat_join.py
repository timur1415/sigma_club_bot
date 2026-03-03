import logging
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence,
    ChatJoinRequestHandler
)

from db.users_crud import get_user

async def chat_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)
    if user and user.sub_status == 'active':
        await update.chat_join_request.approve()