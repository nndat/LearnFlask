from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from myblog.auth.form import LoginForm, RegisterForm
from myblog.models import User
from myblog import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        password = form.password.data
        # if user and user.password == form.password.data:
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=form.remember.data)
            flash('Login success', 'success')
            return redirect(url_for('posts.index'))
        else:
            flash("Username or Password don't correct. "
                  "Please try again", "danger")
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data) \
           .decode('utf-8')
        user = User(username=form.username.data,
                    password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {user.username}. "
              "Your account have create success", "success")
        login_user(user)
        return redirect(url_for('posts.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('posts.index'))
