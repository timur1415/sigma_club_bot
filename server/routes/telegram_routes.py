from fastapi import APIRouter, Request, Response, status
from telegram import Update
from telegram.ext import Application


router = APIRouter()


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    bot_app: Application = request.app.state.bot_app
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)
    return Response(status_code=status.HTTP_200_OK)
