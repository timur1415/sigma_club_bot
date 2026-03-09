from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.logger import logger
from pydantic import BaseModel
import uuid
from config.config import CP_PUBLIC_ID, TOKEN
from db.users_crud import add_email
from db.payment_crud import create_payment
from tools.validate_init_data import validate_init_data

router = APIRouter()


class OrderRequest(BaseModel):
    email: str
    subscription_type: str
    init_data: str


@router.post("/order/")
async def create_order(request: OrderRequest):
    invoice_id = uuid.uuid4()
    logger.info(invoice_id)
    
    logger.info(request.init_data)
    user_data_dict = validate_init_data(request.init_data, TOKEN)
    logger.info(user_data_dict)
    user = await add_email(
        user_data_dict['id'],
        request.email,
    )
    await create_payment(
        user.id,
        user_data_dict['id'],
        request.subscription_type,
        str(invoice_id),
        request.email,
    )
    logger.info(f'платёж создаётся для пользователя с id: {user.id}')
    return JSONResponse({"publicId": CP_PUBLIC_ID, "invoiceId": str(invoice_id)})
