import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
            chat_id=update.effective_chat.id, text="соси соси сделай"
        )
