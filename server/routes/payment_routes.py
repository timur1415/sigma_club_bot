from fastapi import APIRouter, Request, Response, status
from telegram import Update
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.config import SECRET_TOKEN
from config.logger import logger 
router = APIRouter()


@router.post('/pay')
async def first_payment(request: Request):
    data = await request.form()
    logger.info(data)