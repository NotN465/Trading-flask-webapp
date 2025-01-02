from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_user, login_required, logout_user, current_user

portofilo_blueprint = Blueprint('portfolio',__name__)


@portofilo_blueprint.route('/portfolio',methods=['GET','POST'])
@login_required
def portfolio():
    return render_template("portfolio.html",user=current_user)