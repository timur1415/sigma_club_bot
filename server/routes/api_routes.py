from fastapi import APIRouter, Request, Response, status
from telegram import Update
from telegram.ext import Application
from fastapi.responses import FileResponse
from config.logger import logger


router = APIRouter()

@router.post('/order/')
async def create_order(request: Request):
    payload = await request.json()
    email = payload.get('email')
    return Response({'email':email[::-1]})