from flask import Flask, render_template
from markupsafe import escape
from config import app, db
from DB.db_builder import Users



@app.route("/")
def index():
    users = db.session().query(Users).all()
    return  render_template('index.html',posts=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)