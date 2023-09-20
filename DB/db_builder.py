# import sqlalchemy as sql
# from sqlalchemy.orm import sessionmaker, declarative_base
# import os
# from dotenv import load_dotenv
# load_dotenv()
# db_path = 'sqlite:///' + os.getenv("DB_PATH")


from flask_app.config import db, app


# Base = declarative_base()
class Categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(name='category_id', type_=db.Integer, primary_key=True)
    category_title = db.Column(name='category_title', type_=db.String)

    def __init__(self, category_id, category_title):
        self.category_id = category_id
        self.category_title = category_title

    def __repr__(self):
        return f'{self.category_id}, {self.category_title}'


class Subcategories(db.Model):
    __tablename__ = 'subcategories'
    subcategories_id = db.Column(name='subcategories_id', type_=db.Integer, primary_key=True)
    subcategories_categories = db.Column(db.Integer, db.ForeignKey('categories.category_id', ondelete="CASCADE"))
    subcategories_titel = db.Column(name='subcategory_title', type_=db.String)
    subcategories_url = db.Column(name='category_title', type_=db.String, nullable=True)
    
    def __init__(self, subcategories_id,subcategories_categories, subcategories_titel, subcategories_url):
        self.subcategories_id = subcategories_id
        self.subcategories_categories = subcategories_categories
        self.subcategories_titel = subcategories_titel
        self.subcategories_url = subcategories_url
        
    def __repr__(self):
        return f'{self.subcategories_id}, {self.subcategories_categories}, {self.subcategories_titel}, {self.subcategories_url}'


class Channels(db.Model):
    __tablename__ = 'channels'
    channel_id = db.Column(name='channel_id', type_=db.Integer, primary_key=True)
    subcategories_channel = db.Column(db.Integer, db.ForeignKey('subcategories.subcategories_id', ondelete="CASCADE"))
    channel_titel = db.Column(name='channel_titel', type_=db.String)
    channel_url = db.Column(name='channel_url', type_=db.String)
    
    def __init__(self, channel_id, subcategories_channel, channel_titel, channel_url):
        self.channel_id = channel_id
        self.subcategories_channel = subcategories_channel
        self.channel_titel = channel_titel
        self.channel_url = channel_url
    
    def __repr__(self):
        return f'{self.channel_id}, {self.subcategories_channel}, {self.channel_titel}, {self.channel_url}'


class Users(db.Model):
    """_summary_

    table for collecting user data
    """
    __tablename__ = 'users'
    _id = db.Column(name='_id', type_=db.Integer, primary_key=True)
    user_id = db.Column(name='user_id', type_=db.Integer, index=True)
    user_name = db.Column(name='user_name', type_=db.String)
    
    def __init__(self, _id, user_id, user_name):
        self._id = _id
        self.user_id = user_id
        self.user_name = user_name
        
    def __repr__(self):
        return f'{self._id}, {self.user_id}, {self.user_name}'

with app.app_context():
    db.create_all()