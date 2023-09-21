from flask import Flask, render_template
from markupsafe import escape
from config import app, db
from DB.db_builder import Users, Categories, Subcategories, Channels


@app.route("/chanels")
def chanels_html():
    channels = db.session().query(Channels).all()
    return  render_template('chanels.html',posts=channels)


@app.route("/subcategories")
def subcategories_html():
    subcategories = db.session().query(Subcategories).all()
    return  render_template('subcategories.html',posts=subcategories)


@app.route("/categories")
def categories_html():
    users = db.session().query(Categories).all()
    return  render_template('categories.html',posts=users)


@app.route("/users")
def index():
    users = db.session().query(Users).all()
    return  render_template('users.html',posts=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)