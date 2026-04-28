from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)

from db.users_crud import create_user, get_user
from handlers.jobs import job1

# from tools.sup_func import is_channel_subscribed

from config.states import MAIN_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update.effective_user.id)
    if not user:
        user = await create_user(update.effective_user.id, update.effective_user.username)
    # tgk_keyboard = [
    #     [InlineKeyboardButton("подпишись на тгк", url="https://t.me/timik328")],
    #     [InlineKeyboardButton("я подписался", callback_data="sub")],
    # ]

    keyboard = [
        [InlineKeyboardButton("✅вступить в клуб✅", callback_data="join")],
        [InlineKeyboardButton("❓зачем тебе в клуб❓", callback_data="why")],
        [InlineKeyboardButton("💬отзывы💬", url="https://t.me/reviews1264")],
    ]

    # member = await is_channel_subscribed(context, update.effective_user.id)
    # if member == True:
    await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open("photo/hasbik.png", "rb"),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    context.job_queue.run_once(job1, when=5, chat_id=update.effective_chat.id, data={'name':update.effective_user.first_name})
    return MAIN_MENU
    # else:
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text="❌ты не подписан на тгк❌",
    #         reply_markup=InlineKeyboardMarkup((tgk_keyboard)),
    #     )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("💸оплатить💸", callback_data="pay")],
        [
            InlineKeyboardButton(
                "📖прочитать условия📖",
                url="https://telegra.ph/Usloviya-soglasheniya-i-predostavleniya-uslug-IT-BLANKO-05-10",
            )
        ],
        [
            InlineKeyboardButton(
                "💬написать в поддержку💬", url="https://t.me/romanenko_vova"
            )
        ],
        [InlineKeyboardButton("🔙в главное меню🔙", callback_data="main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/car_hasbik.png", "rb"),
        reply_markup=markup,
    )


async def why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("✅вступить в клуб✅", callback_data="join")],
        [InlineKeyboardButton("🔙в главное меню🔙", callback_data="main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("photo/evil_hasbik.png", "rb"),
        caption="Вступай в Клуб Сигма-Пайтонистов!\n\n🐍 Только хардкор: метаклассы, асинхронка и оптимизация под капотом.\n💻 Чат без новичков: если не знаешь, что такое GIL — мимо.\n💰 Сливы вакансий, AI-разборы и автоматизация на максималках.\n\n покупай подписку по нашему прайсу или остаешься в мире print(Hello, world!)\n\nВыбор за тобой, сигма. 😏",
        reply_markup=markup,
    )
