from fastapi import APIRouter, Request, Response, status
from telegram import Update
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.config import SECRET_TOKEN
from config.logger import logger 
from db.payment_crud import get_payment, update_payment
router = APIRouter()

 #тут приходит инфа что кто то оплатил и я проверяю валидность и меняю статус платежа
@router.post('/pay/')
async def first_payment(request: Request):
    data = await request.form()
    logger.info(data)
    status = data.get('Status')
    if status == 'Completed':
        payment = await get_payment(data['InvoiceId'])
        logger.info(payment)
        await update_payment(data['InvoiceId'], 'Completed')
        await request.app.state.bot_app.bot.send_message(chat_id=payment.telegram_id, text='вы успешно оплатили')
      
   