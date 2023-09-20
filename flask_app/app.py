from flask import Flask
from config import app, db
from DB.db_builder import Users




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')