from flask import Flask, render_template,  request, url_for, flash, redirect
from config import app, db
from DB.db_builder import Users, Categories, Subcategories, Channels


@app.route("/chanels")    
def chanels_html():
    channels = db.session().query(Channels).all()
    return render_template('chanels.html',posts=channels)


@app.route("/subcategories")
def subcategories_html():
    subcategories = db.session().query(Subcategories).all()
    return  render_template('subcategories.html',posts=subcategories)


@app.route("/categories", methods=('GET', 'POST'))
def categories_html():
    if request.method == 'POST':
        
        if request.form.get('send_button') and (request.form["categori_name"] != ''):
            categori_name = request.form["categori_name"]
            new_categori = Categories(categori_name)
            db.session.add(new_categori)
            db.session.commit()
            return redirect(url_for('categories_html'))
        
        elif request.form.get('delete_button'):
            delete_id=request.form['delete_button']
            db.session.query(Categories).filter_by(category_id=delete_id).delete()
            db.session.commit()
            return redirect(url_for('categories_html'))
        
        elif request.form.get('change_button'):
            old_id = request.form["change_button"]
            category_update = db.session.query(Categories).filter_by(category_id=old_id).one()
            category_update.category_id = request.form["cat_id"]
            category_update.category_title = request.form["cat_title"]
            db.session.commit()
            return redirect(url_for('categories_html'))
        
    users = db.session().query(Categories).order_by(Categories.view_order).all()
    return render_template('categories.html', posts=users)


@app.route("/users")
def index():
    users = db.session().query(Users).all()
    return render_template('users.html', posts=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)