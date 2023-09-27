from flask_app.config import db, app, login_manager
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from flask_login import UserMixin

class Categories(db.Model):

    __tablename__ = 'categories'
    category_id = Column(name='category_id', type_=db.Integer, primary_key=True, autoincrement=True)
    category_title = Column(name='category_title', type_=db.String)
    view_order = Column(name='view_order', type_=db.Integer)
    subcategories = relationship('Subcategories', backref='categories', cascade="all, delete-orphan, save-update, merge")
    def __init__(self, category_title):
        self.category_title = category_title
        with app.app_context():
            self.view_order = db.session().query(Categories).count() + 1

    def __repr__(self):
        return f'{self.category_id}, {self.category_title}, {self.view_order}'


class Subcategories(db.Model):
    __tablename__ = 'subcategories'
    subcategories_id = Column(name='subcategories_id', type_=db.Integer, primary_key=True)
    subcategories_categories = Column(db.Integer, ForeignKey('categories.category_id', ondelete='CASCADE'))
    subcategories_titel = Column(name='subcategories_titel', type_=db.String)
    subcategories_url = Column(name='subcategories_url', type_=db.String, default=None)
    view_order = Column(name='view_order', type_=db.Integer, autoincrement=True)
    channel = relationship('Channels', cascade="all, delete-orphan, save-update, merge", backref='subcategories')

    def __init__(self, subcategories_categories, subcategories_titel, subcategories_url):
        self.subcategories_categories = subcategories_categories
        self.subcategories_titel = subcategories_titel
        self.subcategories_url = subcategories_url
        with app.app_context():
            self.view_order = db.session().query(Subcategories).where(Subcategories.subcategories_categories == subcategories_categories).count() + 1

    def __repr__(self):
        return f'{self.subcategories_id}, {self.subcategories_categories}, {self.subcategories_titel}, {self.subcategories_url}, {self.view_order}'


class Channels(db.Model):
    __tablename__ = 'channels'
    channel_id = Column(name='channel_id', type_=db.Integer, primary_key=True)
    subcategories_channel = Column(db.Integer, ForeignKey('subcategories.subcategories_id', ondelete='CASCADE'))
    channel_titel = Column(name='channel_titel', type_=db.String)
    channel_url = Column(name='channel_url', type_=db.String)
    view_order = Column(name='view_order', type_=db.Integer, autoincrement=True)

    def __init__(self, subcategories_channel, channel_titel, channel_url):
        self.subcategories_channel = subcategories_channel
        self.channel_titel = channel_titel
        self.channel_url = channel_url
        self.display_order = self.channel_id
        with app.app_context():
            self.view_order = db.session().query(Channels).where(Channels.subcategories_channel==subcategories_channel).count() + 1

    def __repr__(self):
        return f'{self.channel_id}, {self.subcategories_channel}, {self.channel_titel}, {self.channel_url}'


class Users(UserMixin, db.Model):
    """_summary_

    table for collecting user data
    """
    tablename = 'users'
    _id = Column(name='_id', type_=db.Integer, primary_key=True,)
    user_id = Column(name='user_id', type_=db.Integer, index=True)
    user_name = Column(name='user_name', type_=db.String)
    password = Column(name='password', type_=db.String)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return f'{self._id}, {self.user_id}, {self.user_name}'

    def get_id(self):
        return str(self.user_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
