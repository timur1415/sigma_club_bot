import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence
)

from config.config import TOKEN

from handlers.common_handler import start

from config.states import MAIN_MENU

from handlers.common_handler import join, why

from handlers.payment_handler import pay

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)



if __name__ == "__main__":
    persistence = PicklePersistence(filepath="club_bot")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    conv_hadler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(join, 'join'),
                CallbackQueryHandler(pay, 'pay'),
                CallbackQueryHandler(start, 'sub'),
                CallbackQueryHandler(why, 'why'),
                CallbackQueryHandler(start, 'main_menu')
            ]
        },
        name="club_bot",
        persistent=True,
        fallbacks=[CommandHandler("start", start)]
    )
    
    
    application.add_handler(conv_hadler)

    application.run_polling()
