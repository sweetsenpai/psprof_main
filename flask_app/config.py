import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()
db_path = 'sqlite:///' + os.getenv("DB_PATH")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path + '/admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

