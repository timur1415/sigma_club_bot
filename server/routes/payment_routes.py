from fastapi import APIRouter, Request, Response, status
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.config import GROUP_URL, SECRET_TOKEN
from config.logger import logger
from db.payment_crud import get_payment, update_payment
from db.users_crud import update_user_substatus

router = APIRouter()


# тут приходит инфа что кто то оплатил и я проверяю валидность и меняю статус платежа
@router.post("/pay/")
async def first_payment(request: Request):
    keyboard = [[InlineKeyboardButton("Перейти в канал", url=GROUP_URL)]]
    markup = InlineKeyboardMarkup(keyboard)
    data = await request.form()
    logger.info(data)
    status_data = data.get("Status")
    if status_data == "Completed":
        payment = await get_payment(data["InvoiceId"])
        logger.info(payment)
        await update_payment(data["InvoiceId"], "completed")
        await update_user_substatus(payment.telegram_id, 'active')
        await request.app.state.bot_app.bot.send_message(
            chat_id=payment.telegram_id, text="вы успешно оплатили", reply_markup=markup
        )
    return Response(status_code=status.HTTP_200_OK)


@router.post("/fail/")
async def fail_payment(request: Request):
    data = await request.form()
    logger.info(data)
    status = data.get("Status")
    payment = await get_payment(data["InvoiceId"])
    await update_payment(data["InvoiceId"], "Failed")
    await request.app.state.bot_app.bot.send_message(
        chat_id=payment.telegram_id, text="оплата не прошла"
    )
    return Response(status_code=status.HTTP_200_OK)
