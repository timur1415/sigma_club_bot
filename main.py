import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)

from config.config import TOKEN

from handlers.common_handler import start

from config.states import MAIN_MENU

from handlers.common_handler import join

from handlers.payment_handler import pay

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)



if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(join, 'join'),
                CallbackQueryHandler(pay, 'pay'),
                CallbackQueryHandler(start, 'sub')
            ]
        },
        fallbacks=[CommandHandler("start", start)]
        )
    
    
    application.add_handler(conv_hadler)

    application.run_polling()
