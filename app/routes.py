from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, resalepriceinputform
from flask_login import current_user, login_user
from app.models import User, resaleInput
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',title='home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/buyer/<username>')
@login_required
def buyer(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('buyer.html', user=user)

@app.route('/seller/<username>')
@login_required
def seller(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('seller.html', user=user)

@app.route('/resalepriceestimator/<username>',methods=['GET', 'POST'])
@login_required
def resalepriceestimator(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = resalepriceinputform()
    if form.validate_on_submit():
        rsinput = resaleInput(town=form.town.data,flatType=form.flatType.data, ogprice=form.ogprice.data,
        floorArea=form.floorArea.data, storey=form.storey.data, age=form.age.data, user_id = user.id)
        db.session.add(rsinput)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('resalepriceestimator.html', user=user, form=form)

@app.route('/flatpriceestimator/<username>')
@login_required
def flatpriceestimator(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('flatpriceestimator.html', user=user)

@app.route('/townrecommender/<username>')
@login_required
def townrecommender(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('townrecommender.html', user=user)

@app.route('/delete/<username>')
@app.route('/delete/<username>/<id>')
@login_required
def delete(username, id):
    user = User.query.filter_by(username=username).first_or_404()
    ID = resaleInput.query.filter_by(id=id).first_or_404()
    db.session.delete(ID)
    db.session.commit()
    return render_template('user.html', user=user)

