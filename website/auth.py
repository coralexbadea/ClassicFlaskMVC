from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category="alert")
        else:
            flash("No account for the entered email", category="alert")

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password = request.form.get('password')
        password1 = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("There is already an account with this email", category="alert")
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error') 
        elif password != password1:
            flash('Passwords dont\'t match', category='error') 
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login.', category='success')
            return redirect(url_for('views.login'))

    return render_template("sign_up.html", user=current_user)