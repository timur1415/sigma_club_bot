from telegram import Update

from config.config import WEBHOOK_URL, TELEGRAM_WEBHOOK_PATH, SECRET_TOKEN

from fastapi import FastAPI
from contextlib import asynccontextmanager

from handlers.bot_init import create_bot_app
from config.logger import logger

from server.routes import telegram_router
from server.routes import api_router


def init_fastapi_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(telegram_router) 
    app.include_router(api_router, prefix='/api')
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
    
    logger.info('Приложение инициализированно')
    yield
    # что будет происходить при выходе
    try:
        await bot_app.bot.delete_webhook()
    finally:
        await bot_app.stop()
        await bot_app.shutdown()

