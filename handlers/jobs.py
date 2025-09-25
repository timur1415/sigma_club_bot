from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext
)
async def check_payment(context: CallbackContext):
    job = context.job
    payment = job.data['payment_1']
    if payment.paid:
        await context.bot.send_message(chat_id = job.user_id, text = 'вы успешно оплатили')