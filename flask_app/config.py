import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
db_path = 'sqlite:///' + os.getenv("DB_PATH")

app =  Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = db_path + '/admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('PASSWORD')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

