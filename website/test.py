from binance.client import Client

client = Client()


prices = {'bitcoin': client.get_symbol_ticker(symbol='BTCUSDT')['price'],
          'ethereum': client.get_symbol_ticker(symbol='ETHUSDT')['price'],
          'cardano': client.get_symbol_ticker(symbol='ADAUSDT')['price'],
          'ripple': client.get_symbol_ticker(symbol='XRPUSDT')['price'],
          'solana': client.get_symbol_ticker(symbol='SOLUSDT')['price']}
print(prices)