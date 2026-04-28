from telegram.ext import (
    ContextTypes,
)
from config.logger import logger

from db.users_crud import get_all_debtors, update_all_debtors

from config.config import TGK_ID


async def chek_sub_status(context: ContextTypes.DEFAULT_TYPE):
    debtors = await get_all_debtors()
    for dept in debtors:
        logger.info(dept.telegram_id)
        try:
            await context.bot.ban_chat_member(chat_id=TGK_ID, user_id=dept.telegram_id)
            await context.bot.unban_chat_member(
                chat_id=TGK_ID, user_id=dept.telegram_id
            )
            await context.bot.send_message(
                chat_id=dept.telegram_id,
                text="вы были исключены из клуба за неуплату, если вы оплатили, свяжитесь с поддержкой",
            )
        except Exception as e:
            logger.error(f"Ошибка при исключении пользователя {dept.telegram_id}: {e}")
    await update_all_debtors()


async def job1(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f"Привет {context.job.data.get('name')}, это тестовое сообщение от планировщика задач!",
    )
