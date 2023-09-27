from flask import Flask, render_template,  request, url_for, flash, redirect
from flask_login import login_user
from config import app, db
from DB.db_builder import Users, Categories, Subcategories, Channels
import os
from dotenv import load_dotenv
load_dotenv()

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
        
        elif request.form.get('delete_button'):
            delete_id = request.form['delete_button']
            del_member = db.session.query(Categories).filter_by(category_id=delete_id).one()
            db.session.delete(del_member)
            db.session.commit()
        
        elif request.form.get('change_button'):
            update_id = request.form["change_button"]
            category_update = db.session.query(Categories).filter_by(category_id=update_id).one()
            category_update.view_order = request.form["cat_view"]
            category_update.category_title = request.form["cat_title"]
            db.session.commit()
            
        return redirect(url_for('categories_html'))
        
    users = db.session().query(Categories).order_by(Categories.view_order).all()
    return render_template('categories.html', posts=users)


@app.route('/<int:category_id>/subedit', methods=('GET', 'POST'))
def subedit(category_id):
    if request.method == 'POST':
        if request.form.get('send_button'):
            new_sub = Subcategories(category_id,request.form['subcategories_titel'], request.form['subcategories_url'])
            db.session.add(new_sub)
            db.session.commit()
        if request.form.get('delete_button'):
            delete_id = request.form['delete_button']
            del_member = db.session.query(Subcategories).filter_by(subcategories_id=delete_id).delete()
            db.session.delete(del_member)
            db.session.commit()
        if request.form.get('change_button'):
            update_id = request.form["change_button"]
            sub_title = request.form["sub_title"]
            sub_url = request.form["sub_url"]
            sub_veiw =  request.form["sub_view"]
            update_obj = db.session.query(Subcategories).where(Subcategories.subcategories_id==update_id).one_or_none()
            update_obj.subcategories_titel = sub_title
            update_obj.subcategories_url = sub_url
            update_obj.view_order = sub_veiw
            db.session.commit()
        return redirect(f'/{category_id}/subedit')
    subc = db.session.query(Subcategories).where(Subcategories.subcategories_categories == category_id).order_by(Subcategories.view_order).all()
    return render_template('subedit.html', posts=subc)


@app.route('/<int:category_id>/<int:subcategories_id>/chaedit', methods=('GET', 'POST'))
def chaedit(subcategories_id, category_id):
    if request.method == 'POST':
        if request.form.get('send_button'):
            new_cha = Channels(subcategories_id,request.form['channel_titel'], request.form['channel_url'])
            db.session.add(new_cha)
            db.session.commit()
        
        if request.form.get('delete_button'):
            delete_id = request.form['delete_button']
            del_member = db.session.query(Channels).where(Channels.channel_id==delete_id).one_or_none()
            db.session.delete(del_member)
            db.session.commit()
            
        if request.form.get('change_button'):
            update_id = request.form["change_button"]
            cha_title = request.form["cha_titel"]
            cha_url = request.form["cha_url"]
            update_obj = db.session.query(Channels).where(Channels.channel_id == update_id).one_or_none()
            update_obj.channel_titel = cha_title
            update_obj.channel_url = cha_url
            db.session.commit()
        return redirect(f'/{subcategories_id}/{category_id}/chaedit')   
    
    chanels = db.session.query(Channels).where(Channels.subcategories_channel == subcategories_id).order_by(Channels.view_order).all()
    return render_template('chaedit.html', posts=chanels)

@app.route("/users")
def index():
    users = db.session().query(Users).all()
    return render_template('users.html', posts=users)


@app.route('/login', methods=('GET', 'POST'))
def login_post():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        print('-------------------------------------')
        if username!=os.getenv("USERNAME") or password!=os.getenv("PASSWORD"):
            flash('Please check your login details and try again.')
            
        return redirect(url_for('index'))
        
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    