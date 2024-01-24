
import ccxt

# Create an instance of the Bybit exchange
exchange = ccxt.bybit({
    'apiKey': 'SfSjRXrG0onYQG03db',
    'secret': 'dhlEufCbRidVNfcsD9bJ4wbwUbA1AVYpT0XO',
})

currency = 'USDT'       # Replace with the currency you want to withdraw
amount = 10         # Replace with the amount you want to withdraw
address = 'TKxnRRynapdLX2F7azaSYuW3RKipiFF9wE'  # Replace with the withdrawal address
params = {
        'chain': 'TRX',
        "forceChain": 1,
        "accountType": "SPOT"
}
# Create the withdrawal request
withdrawal = exchange.withdraw(
    currency,
    amount,
    address,
    params
)

print(withdrawal)