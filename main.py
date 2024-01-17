import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, Filters, CallbackContext


from keyboards import regions_btn, district_btn, main_btn
from utils import get_district_data, one_week, today_weather as weather_today
from db import Database

# Database
db = Database('main.db')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

REGION_STATE = 1
DISTRTC_STATE = 2


def start(update: Update, context: CallbackContext) -> None:
    btn = regions_btn()
    user = update.effective_user

    if not db.select_user(telegram_id=user.id):

        update.message.reply_text(
            f"Assalomu aleykum {user.mention_html()}\n"
            f"Pasdagi Viloyatlardan birini tanlang ⬇️",
            parse_mode='HTML',
            reply_markup=btn,
        )
        return REGION_STATE

    update.message.reply_text(
        f"Assalomu aleykum {user.mention_html()}\n",
        reply_markup=main_btn(),
        parse_mode='HTML',
    )


def change_region(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hududni tanglang ", reply_markup=regions_btn())
    return REGION_STATE


def region_select(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    region_id = query.data.split("=")[1]
    btn = district_btn(region_id=region_id)
    update.callback_query.message.edit_text(
        "Hududni tanglang ", reply_markup=btn)

    return DISTRTC_STATE


def district_select(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user = update.effective_user
    district_id = query.data.split("=")[1]
    if district_id == "back":
        update.callback_query.message.edit_text(
            "Pasdagi Viloyatlardan birini tanlang ⬇️", reply_markup=regions_btn())
        return REGION_STATE

    district_data = get_district_data(district_id=district_id)

    if not db.select_user(telegram_id=user.id):
        db.add_user(full_name=user.full_name, telegram_id=user.id,
                    country=district_data['data'])

    db.update_user(telegram_id=user.id, country=district_data['data'])

    update.callback_query.message.edit_text(
        f"Siz {district_data['name_uz']}ni tanladingiz", reply_markup=None)

    return ConversationHandler.END


def today_weather(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_data = db.select_user(telegram_id=user.id)

    if not user_data:
        update.message.reply_text(
            "Sizning viloyat tanlamadingiz!", reply_markup=regions_btn())
        return REGION_STATE

    today_weather_data, icon = weather_today(user_data[2])

    image_url = f"https://openweathermap.org/img/wn/{icon}@4x.png"

    text = f"Bugungi ob-havo ⛅️\n\n"
    text += f"Hudud: <b>{user_data[2]}</b>\n"
    text += f"{today_weather_data}"

    update.message.reply_photo(
        photo=image_url, caption=text, parse_mode='HTML')


def one_week_weather(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_data = db.select_user(telegram_id=user.id)

    if not user_data:
        update.message.reply_text(
            "Sizning viloyat tanlamadingiz!", reply_markup=regions_btn())
        return REGION_STATE

    week_weather_data = one_week(user_data[2])

    text = f"Bugungi ob-havo ⛅️\n\n"
    text += f"Hudud: <b>{user_data[2]}</b>\n\n"
    text += f"{week_weather_data}"

    update.message.reply_text(text, parse_mode='HTML')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(
        "5177104446:AAEJWX4QdWkPOsrjHV5MJOEN3GUFzs2k1Oo", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^Bugungi ob-havo ⛅️$'), today_weather))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^1 haftalik ob-havo ⛅️$'), one_week_weather))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('region', change_region),
            MessageHandler(Filters.regex(
                "^Manzilni o'zgartirish ✏️"), change_region)
        ],
        states={
            REGION_STATE: [
                CallbackQueryHandler(region_select, pattern="^region="),
            ],
            DISTRTC_STATE: [
                CallbackQueryHandler(district_select, pattern="^district="),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    dispatcher.add_handler(conv_handler)

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    try:
        db.create_table_users()
    except Exception as error:
        pass

    updater.idle()


if __name__ == '__main__':
    main()
