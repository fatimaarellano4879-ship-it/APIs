from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
from models import User 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('juegos'))
        flash("Usuario o contraseña incorrectos")
    return render_template("login.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada")
    return redirect(url_for('auth.login'))