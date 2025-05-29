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

from start import start

from config.states import MAIN_MENU

from main_work.join import join

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)



if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(join, 'join')
            ]
        },
        fallbacks=[CommandHandler("start", start)]
        )
    
    
    application.add_handler(conv_hadler)

    application.run_polling()
