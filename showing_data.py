import matplotlib.pyplot as plt
import numpy as np
import json

with open('crypto prices.json', 'r') as f:
    json_data = json.load(f)
    bitcoin = json_data['bitcoin']
    ethereum = json_data['ethereum']
    cardano = json_data['cardano']
    ripple = json_data['ripple']
    solana = json_data['solana']

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].plot(bitcoin,color='gold')
axes[0, 0].set_title('Bitcoin')

axes[0, 1].plot(ethereum,color='gray')
axes[0, 1].set_title('Ethereum')

axes[1, 0].plot(cardano,color='blue')
axes[1, 0].set_title('Cardano')

axes[1, 1].plot(ripple,color='blue')
axes[1, 1].set_title('Ripple')


plt.tight_layout()
plt.show()