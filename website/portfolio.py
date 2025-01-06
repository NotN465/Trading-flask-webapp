from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import CryptoCoin, User
from binance.client import Client

Session = sessionmaker(bind=create_engine('sqlite:///C:/Users/Korisnik/PycharmProjects/pythonProject/Trading app/Trading-flask-webapp/instance/database.db'))
session = Session()
portofilo_blueprint = Blueprint('portfolio',__name__)
client = Client('','')

def convert_to_name(value):
    return value.name
@portofilo_blueprint.route('/portfolio',methods=['GET','POST'])
@login_required
def portfolio():
    print(current_user.email,current_user.first_name)
    user = session.query(User).filter_by(email=current_user.email).first()
    coins = session.query(CryptoCoin).filter_by(user=user).all()
    coins_name = list(map(convert_to_name,session.query(CryptoCoin).filter_by(user=user).all()))
    coin_price = []
    len_coins=len(coins)
    coins_amount = []
    last_days = []
    difference = []
    for coin in coins:
        coin_price.append(round(float(coin.price)*float(client.get_symbol_ticker(symbol=coin.name)['price']),2))
        coins_amount.append(round(float(coin.price),2))
    for coin_name in coins_name:
        klines = client.get_klines(symbol=coin_name, interval=Client.KLINE_INTERVAL_1DAY, limit=2)
        last_day_price = klines[0][4]
        last_days.append(float(last_day_price))
    real_prices = []
    for coin in coins:
        real_prices.append(round(float(client.get_symbol_ticker(symbol=coin.name)['price']),2))
    for i in range(len(real_prices)):
        if float(last_days[i]) > float(real_prices[i]):
            difference.append(f"-{((float(last_days[i])/float(real_prices[i]))-1)*100:.2f}%")
        else:
            difference.append(f"+{(float(real_prices[i])/float(last_days[i])-1)*100:.2f}%")
    print(last_days,real_prices)
    print(difference)

    return render_template("portfolio.html",user=current_user,firstname=user.first_name,coins=coins_name,coins_amount=coins_amount,coins_price=coin_price,len_coins=len_coins,difference=difference)