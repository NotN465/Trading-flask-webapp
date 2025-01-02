from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from binance.client import Client
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from .models import CryptoCoin,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
client = Client()
trade_blueprint = Blueprint('trade',__name__)
engine = create_engine('sqlite:///D:/pythonProject1/Flask trading app/instance/database.db')
Session = sessionmaker(bind=engine)
session = Session()

submited = False
@trade_blueprint.route('/trade',methods=['GET','POST'])
@login_required
def trade():
    global submited
    if request.method == "POST":

        submited = True
        form_data = request.form.to_dict()
        print(form_data)
        if 'time' in form_data:

            time = list(form_data.values())[0]
            print(time,submited)
            with open('website/symbol.txt', 'r') as f:
                symbol = f.read()
            symbol = symbol + "USDT"
            interval = check_time(time)
            with open('website/time.txt', 'w') as f:
                f.write(time)
            graph_html = make_graph(symbol,interval)
            return render_template("trade.html", graph_html=graph_html, user=current_user,current_symbol=symbol)

        elif 'symbol' in form_data:

            submited = True
            symbol = form_data.get("symbol")
            with open('website/symbol.txt', 'w') as f:
                f.write(symbol)
            symbol = symbol + "USDT"
            interval = Client.KLINE_INTERVAL_1HOUR
            graph_html = make_graph(symbol,interval)
            return render_template("trade.html", graph_html=graph_html, user=current_user,current_symbol=symbol)

        elif 'buy' in form_data:

            #loading the website
            with open('website/symbol.txt', 'r') as f:
                symbol = f.read()
            if symbol == '':
                symbol = 'BTCUSDT'
            else:
                symbol = symbol + "USDT"
            with open('website/time.txt', 'r') as f:
                time = f.read()
            if time=='':
                time = '1HOUR'
            else:
                time = time
            interval = check_time(time)
            graph_html = make_graph(symbol,interval)

            #updating the database
            user = session.query(User).filter_by(email=current_user.email).first()
            crypto_coins = session.query(CryptoCoin).filter_by(user_id=user.id).all()
            def convert_to_str(crypto_coin):
                return crypto_coin.name
            crypto_coins = list(map(convert_to_str,crypto_coins))
            if symbol not in crypto_coins:
                crypto_coin = CryptoCoin(name=symbol,price=form_data["buy"],user_id=user.id)
                session.add(crypto_coin)
                session.commit()
            else:

                crypto_coin = session.query(CryptoCoin).filter_by(user_id=user.id,name=symbol).first()
                coin_price=client.get_symbol_ticker(symbol=symbol)['price']
                crypto_coin.price = float(form_data["buy"])/float(coin_price)+float(crypto_coin.price)
                session.commit()


            return render_template("trade.html", graph_html=graph_html, user=current_user,current_symbol=symbol)

        elif 'sell' in form_data:


            #loading the website
            with open('website/symbol.txt', 'r') as f:
                symbol = f.read()
            if symbol == '':
                symbol = 'BTCUSDT'
            else:
                symbol = symbol + "USDT"
            with open('website/time.txt', 'r') as f:
                time = f.read()
            if time=='':
                time = '1HOUR'
            else:
                time = time
            interval = check_time(time)
            graph_html = make_graph(symbol,interval)
            #updating the database
            print("selling: " + form_data["sell"])
            user = session.query(User).filter_by(email=current_user.email).first()
            crypto_coins = session.query(CryptoCoin).filter_by(user_id=user.id).all()
            def convert_to_str(crypto_coin):
                return crypto_coin.name
            crypto_coins = list(map(convert_to_str,crypto_coins))
            if symbol not in crypto_coins:
                flash("Buy the coin first",category="error")
            else:
                crypto_coin = session.query(CryptoCoin).filter_by(user_id=user.id,name=symbol).first()
                coin_price=client.get_symbol_ticker(symbol=symbol)['price']
                if float(crypto_coin.price) > float(form_data["sell"])/float(coin_price):
                    crypto_coin.price = float(crypto_coin.price)-float(form_data["sell"])/float(coin_price)
                    session.commit()
                else:
                    flash("Not enough coins",category="error")
            return render_template("trade.html", graph_html=graph_html, user=current_user,current_symbol=symbol)

    return render_template("trade.html", user=current_user)
def make_graph(symbol,interval):
    limit = 100
    candlesticks = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    data = {'Timestamp': [], 'Open': [], 'High': [], 'Low': [], 'Close': []}
    for candlestick in candlesticks:
        data['Timestamp'].append(candlestick[0])
        data['Open'].append(candlestick[1])
        data['High'].append(candlestick[2])
        data['Low'].append(candlestick[3])
        data['Close'].append(candlestick[4])
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    print(df)
    print(symbol, submited)

    fig = go.Figure(
        data=[go.Candlestick(x=df['Timestamp'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(title='Candlestick Chart', xaxis_title='Timestamp', yaxis_title='Price')
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html
def check_time(time):
    if time == '1HOUR':
        interval = Client.KLINE_INTERVAL_1HOUR
    elif time == '12HOUR':
        interval = Client.KLINE_INTERVAL_12HOUR
    elif time == '1DAY':
        interval = Client.KLINE_INTERVAL_1DAY
    elif time == '1WEEK':
        interval = Client.KLINE_INTERVAL_1WEEK
    elif time == '1MONTH':
        interval = Client.KLINE_INTERVAL_1MONTH
    else:
        interval = Client.KLINE_INTERVAL_1HOUR
    return interval