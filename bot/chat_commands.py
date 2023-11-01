from telegram.ext import ContextTypes
from sqlalchemy import or_
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from DB.db_builder import Categories, Subcategories, Channels, db, Users
from flask_app.config import app


async def show_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        chats_list = []
        with app.app_context():
            chats = db.session.query(Subcategories).where(Subcategories.subcategories_categories == 2).order_by(Subcategories.view_order).all()
        for chat in chats:
            chats_list.append([InlineKeyboardButton(text=chat.subcategories_titel, url=chat.subcategories_url)])
        await update.message.reply_text(text='Чаты Петроградского района:', reply_markup=InlineKeyboardMarkup(chats_list))
    return


async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        channels_list = []
        with app.app_context():
            channels = db.session.query(Subcategories).where(Subcategories.subcategories_categories == 3).order_by(Subcategories.view_order).all()
        for channel in channels:
            channels_list.append([InlineKeyboardButton(text=channel.subcategories_titel, url=channel.subcategories_url)])
        await update.message.reply_text(text='Каналы Петроградского района:', reply_markup=InlineKeyboardMarkup(channels_list))
    return
