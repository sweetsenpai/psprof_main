from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update
import logging
import os
from menu import main_menu, sub_menu, channels_menu, back
# from dotenv import load_dotenv
# load_dotenv()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '50'))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello world!')
    return


def main() -> None:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', main_menu))
    application.add_handler(CallbackQueryHandler(pattern='MAIN', callback=main_menu))
    application.add_handler(CallbackQueryHandler(pattern='M:', callback=sub_menu))
    application.add_handler(CallbackQueryHandler(pattern='S:', callback=channels_menu))
    application.add_handler(CallbackQueryHandler(pattern='BACK:', callback=back))
    application.run_polling()


if __name__ == '__main__':

    main()
