from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.logger import logger
from pydantic import BaseModel
import uuid
from config.config import CP_PUBLIC_ID
from db.users_crud import add_email
from db.payment_crud import create_payment

router = APIRouter()


class OrderRequest(BaseModel):
    email: str
    telegram_id: int
    subscription_type: str


@router.post("/order/")
async def create_order(request: OrderRequest):
    invoice_id = uuid.uuid4()
    logger.info(invoice_id)
    user = await add_email(
        request.telegram_id,
        request.email,
    )
    await create_payment(
        user.id,
        request.telegram_id,
        request.subscription_type,
        invoice_id,
        request.email,
    )
    return JSONResponse({"publicId": CP_PUBLIC_ID, "invoiceId": str(invoice_id)})
