import logging
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from config.config import TOKEN, WEBHOOK_URL, TELEGRAM_WEBHOOK_PATH, SECRET_TOKEN
from handlers.common_handler import start

from config.states import MAIN_MENU

from handlers.common_handler import join, why

from handlers.payment_handler import pay

from fastapi import FastAPI, Request, Response, status
from contextlib import asynccontextmanager

from handlers.bot_init import create_bot_app
from config.logger import logger


def init_fastapi_app():
    app = FastAPI(lifespan=lifespan)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # что будет происходить при запуске
    bot_app = create_bot_app()

    app.state.bot_app = bot_app

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(
        url=WEBHOOK_URL + TELEGRAM_WEBHOOK_PATH,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        secret_token=SECRET_TOKEN,
    )
    @app.post("/telegram/webhook")
    async def telegram_webhook(request: Request):
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.update_queue.put(update)
        return Response(status_code=status.HTTP_200_OK)
    logger.info('Приложение инициализированно')
    yield
    # что будет происходить при выходе
    try:
        await bot_app.bot.delete_webhook()
    finally:
        await bot_app.stop()
        await bot_app.shutdown()




