from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from DB.db_builder import Categories, Subcategories, Channels, db
from flask_app.config import app


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with app.app_context():
        categories = db.session.query(Categories).order_by(Categories.view_order).all()
    main_list = []
    for cat in categories:
        main_list.append([InlineKeyboardButton(text=cat.category_title, callback_data=f"M:{cat.category_id}")])
    try:
        await update.message.reply_text(text='Выбери категорию', reply_markup=InlineKeyboardMarkup(main_list))
    except AttributeError:
        await update.callback_query.edit_message_text(text='Выбери категорию', reply_markup=InlineKeyboardMarkup(main_list))
    return


def sub_builder(subcategories):
    sub_list = []
    for sub in subcategories:
        if sub.subcategories_url == '':
            sub_list.append(
                [InlineKeyboardButton(text=sub.subcategories_titel, callback_data=f'S:{sub.subcategories_id}')])
        else:
            sub_list.append([InlineKeyboardButton(text=sub.subcategories_titel, url=sub.subcategories_url)])
    sub_list.append([InlineKeyboardButton(text='На главную 🏠', callback_data='MAIN')])
    return sub_list


async def sub_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_id = int(update.callback_query.data.replace('M:', ''))
    with app.app_context():
        subcategories = db.session.query(Subcategories).where(Subcategories.subcategories_categories == cat_id).order_by(Subcategories.view_order).all()
    await update.callback_query.edit_message_text(text='Выбери категорию', reply_markup=InlineKeyboardMarkup(sub_builder(subcategories)))
    return


async def channels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sub_id = int(update.callback_query.data.replace('S:', ''))
    with app.app_context():
        channels = db.session.query(Channels).where(Channels.subcategories_channel == sub_id).order_by(Channels.view_order).all()
    channel_list = []
    for chanel in channels:
        channel_list.append([InlineKeyboardButton(text=chanel.channel_titel, url=chanel.channel_url)])
    channel_list.append([InlineKeyboardButton(text='⬅️Назад', callback_data=f'BACK:{sub_id}'), InlineKeyboardButton(text='На главную 🏠', callback_data='MAIN')])
    await update.callback_query.edit_message_text(text='Выбери категорию', reply_markup=InlineKeyboardMarkup(channel_list))
    return


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    back_id = int(update.callback_query.data.replace('BACK:', ''))
    with app.app_context():
        sub_id = db.session.query(Subcategories).where(Subcategories.subcategories_id == back_id).one_or_none()
        cat_id = sub_id.subcategories_categories
        subcategories = db.session.query(Subcategories).where(Subcategories.subcategories_categories == cat_id).order_by(Subcategories.view_order).all()
    await update.callback_query.edit_message_text(text='Выбери категорию', reply_markup=InlineKeyboardMarkup(sub_builder(subcategories)))
    return
