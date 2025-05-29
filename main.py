import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
)

from config.config import TOKEN

from start import start

from config.states import MAIN_MENU

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)



if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: []
        })
    
    
    application.add_handler(conv_hadler)

    application.run_polling()
