from flask import Flask, render_template,  request, url_for, flash, redirect
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import and_
from config import app, db, login_manager
from DB.db_builder import Users, Categories, Subcategories, Channels
import datetime
from dotenv import load_dotenv
load_dotenv()

@app.route("/chanels")
@login_required    
def chanels_html():
    channels = db.session().query(Channels).all()
    return render_template('chanels.html',posts=channels)


@app.route("/subcategories")
@login_required  
def subcategories_html():
    subcategories = db.session().query(Subcategories).all()
    return  render_template('subcategories.html',posts=subcategories, name=current_user.user_id)


@app.route("/categories", methods=('GET', 'POST'))
@login_required  
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
    return render_template('categories.html', posts=users, name=current_user.user_id)


@app.route('/<int:category_id>/subedit', methods=('GET', 'POST'))
@login_required  
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
    return render_template('subedit.html', posts=subc, name=current_user.user_id)


@app.route('/<int:category_id>/<int:subcategories_id>/chaedit', methods=('GET', 'POST'))
@login_required  
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
    return render_template('chaedit.html', posts=chanels, name=current_user.user_id)

@app.route("/users")
@login_required  
def users():
    users = db.session().query(Users).all()
    return render_template('users.html', posts=users, name=current_user.user_id)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(int(user_id))


@login_manager.unauthorized_handler 
def unauthorized_callback():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        user = db.session.query(Users).where(and_(Users.user_name == username, Users.password == password)).one_or_none()
        if not user:
            flash('Please check your login details and try again.', category='error')
            return redirect(url_for('login'))
        
        login_user(user, remember=False, duration=datetime.timedelta(seconds=10))
        flash('Logged in successfully.')
        print('---------------------------------------------')
        return redirect(url_for('categories_html'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    