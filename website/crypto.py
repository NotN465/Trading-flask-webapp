from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_user, login_required, logout_user, current_user
from binance.client import Client
import json

crypto = Blueprint('crypto',__name__)
client = Client()

prev_bitcoin = None
prev_ethereum = None
prev_cardano = None
prev_ripple = None
prev_solana = None

@crypto.route('/coins',methods=['GET','POST'])
@login_required
def crypto_coin():
    prices = {'bitcoin': client.get_symbol_ticker(symbol='BTCUSDT')['price'], 'ethereum': client.get_symbol_ticker(symbol='ETHUSDT')['price'],
              'cardano': client.get_symbol_ticker(symbol='ADAUSDT')['price'],
              'ripple': client.get_symbol_ticker(symbol='XRPUSDT')['price'], 'solana': client.get_symbol_ticker(symbol='SOLUSDT')['price']}
    return render_template("crypto.html",user=current_user,coins=prices)
@crypto.route('/api/coins', methods=['GET'])
@login_required
def get_crypto_prices():
    global prev_bitcoin, prev_ethereum, prev_cardano, prev_ripple, prev_solana
    prices = {'bitcoin': client.get_symbol_ticker(symbol='BTCUSDT')['price'], 'prev_bitcoin': prev_bitcoin,'ethereum': client.get_symbol_ticker(symbol='ETHUSDT')['price'], 'prev_ethereum': prev_ethereum,
              'cardano': client.get_symbol_ticker(symbol='ADAUSDT')['price'], 'prev_cardano': prev_cardano,
              'ripple': client.get_symbol_ticker(symbol='XRPUSDT')['price'], 'prev_ripple': prev_ripple, 'solana': client.get_symbol_ticker(symbol='SOLUSDT')['price'], 'prev_solana': prev_solana}
    prev_bitcoin = prices['bitcoin']
    prev_ethereum = prices['ethereum']
    prev_cardano = prices['cardano']
    prev_ripple = prices['ripple']
    prev_solana = prices['solana']
    '''prices_json = {'bitcoin': prices['bitcoin'], 'ethereum': prices['ethereum'], 'cardano': prices['cardano'], 'ripple': prices['ripple'], 'solana': prices['solana']}
    with open('crypto prices.json', 'r') as f:
        json_data = json.load(f)
        json_data['bitcoin'].append(prices_json['bitcoin'])
        json_data['ethereum'].append(prices_json['ethereum'])
        json_data['cardano'].append(prices_json['cardano'])
        json_data['ripple'].append(prices_json['ripple'])
        json_data['solana'].append(prices_json['solana'])
    with open('crypto prices.json', 'w') as f:
        json.dump(json_data, f, indent=4)
    '''

    return jsonify(prices)