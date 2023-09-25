from flask_app.config import db, app
from sqlalchemy.orm import sessionmaker, relationship


class Categories(db.Model):
    
    __tablename__ = 'categories'
    category_id = db.Column(name='category_id', type_=db.Integer, primary_key=True)
    category_title = db.Column(name='category_title', type_=db.String)
    subcategories = relationship('Subcategories', backref='categories', cascade='save-update, merge, delete')

    def __init__(self, category_title):
        self.category_title = category_title

    def __repr__(self):
        return f'{self.category_id}, {self.category_title}'


class Subcategories(db.Model):
    __tablename__ = 'subcategories'
    subcategories_id = db.Column(name='subcategories_id', type_=db.Integer, primary_key=True)
    subcategories_categories = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    subcategories_titel = db.Column(name='subcategories_titel', type_=db.String)
    subcategories_url = db.Column(name='subcategories_url', type_=db.String, default='')
    channels = relationship('Channels', backref='subcategories', cascade='save-update, merge, delete')

    def __init__(self, subcategories_categories, subcategories_titel, subcategories_url):
        self.subcategories_categories = subcategories_categories
        self.subcategories_titel = subcategories_titel
        self.subcategories_url = subcategories_url
        
    def __repr__(self):
        return f'{self.subcategories_id}, {self.subcategories_categories}, {self.subcategories_titel}, {self.subcategories_url}, {self.display_order}'


class Channels(db.Model):
    __tablename__ = 'channels'
    channel_id = db.Column(name='channel_id', type_=db.Integer, primary_key=True)
    subcategories_channel = db.Column(db.Integer, db.ForeignKey('subcategories.subcategories_id'))
    channel_titel = db.Column(name='channel_titel', type_=db.String)
    channel_url = db.Column(name='channel_url', type_=db.String)
    
    def __init__(self, subcategories_channel, channel_titel, channel_url):
        self.subcategories_channel = subcategories_channel
        self.channel_titel = channel_titel
        self.channel_url = channel_url
        self.display_order = self.channel_id
    
    def __repr__(self):
        return f'{self.channel_id}, {self.subcategories_channel}, {self.channel_titel}, {self.channel_url}'


class Users(db.Model):
    """_summary_

    table for collecting user data
    """
    __tablename__ = 'users'
    _id = db.Column(name='_id', type_=db.Integer, primary_key=True,)
    user_id = db.Column(name='user_id', type_=db.Integer, index=True)
    user_name = db.Column(name='user_name', type_=db.String)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return f'{self._id}, {self.user_id}, {self.user_name}'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
