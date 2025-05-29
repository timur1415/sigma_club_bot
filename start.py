from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)

from tools.sup_func import is_channel_subscribed

from config.states import MAIN_MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tgk_keyboard = [[InlineKeyboardButton("подпишись на тгк", url="https://t.me/timik328")]]

    keyboard = [[InlineKeyboardButton('вступить в клуб', callback_data='join')]]
    
    member = await is_channel_subscribed(context, update.effective_user.id)
    if member == True:
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="ты не в клубе", reply_markup= InlineKeyboardMarkup(tgk_keyboard)
        )
        return MAIN_MENU
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="ты не в клубе", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    

