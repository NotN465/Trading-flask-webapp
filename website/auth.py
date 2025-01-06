from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

auth = Blueprint('auth',__name__)

engine = create_engine('sqlite:///C:/Users/Korisnik/PycharmProjects/pythonProject/Trading app/Trading-flask-webapp/instance/database.db')
Session = sessionmaker(bind=engine)
session = Session()

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email =request.form.get("email")
        password = request.form.get("password")

        user = session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in!",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again",category="error")
        else:
            flash("Email does not exist",category="error")

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("FirstName")
        password = request.form.get("password1")
        password_confirm = request.form.get("password2")
        if len(email) < 4:
            flash("Email must be greater than 3 characters",category="error")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters",category="error")
        elif len(password) < 7:
            flash("Password must be greater than 6 characters",category="error")
        elif password != password_confirm:
            flash("Passwords don't match",category="error")
        else:
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password, method="scrypt"))
            if session.query(User).filter_by(email=email).first() is not None:
                flash("Email address already exists",category="error")
                return redirect(url_for("auth.sign_up"))
            else:
                session.add(new_user)
                session.commit()
                flash("Account created!",category="success")
                login_user(new_user,remember=True)
                return redirect(url_for("views.home"))

    return render_template("signup.html",user=current_user)