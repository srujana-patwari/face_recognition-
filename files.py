import requests
import json
api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5&convert=USD&CMC_PRO_API_KEY=22ff4501-289c-44b0-9cfb-d3e57b2ec10f")
api = json.loads(api_request.content)
print("-------")
print("-------")

coins = [
    {
        "symbol":"BTC",
        "amount_owned": 2,
        "price_per_coin":3500
    },
    {
        "symbol": "LINK",
        "amount_owned": 100,
        "price_per_coin": 2.50
    }
]

total_pl = 0 #tatal profit or loss

for i in range(0, 5):
    for coin in coins:
        if api["data"][i]["symbol"] == coin["symbol"]:
            total_paid = coin["amount_owned"] * coin["price_per_coin"]
            current_value = coin["amount_owned"] * api["data"][i]["quote"]["USD"]["price"]
            pl_percoin = api["data"][i]["quote"]["USD"]["price"] * coin["price_per_coin"]
            total_pl_coin = pl_percoin * coin["amount_owned"]

            total_pl = total_pl + total_pl_coin

            print(api["data"][i]["name"]+ "-" +api["data"][i]["symbol"])
            print("price-${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
            print("number of coin:",coin["amount_owned"])
            print("Total amount paid:", "${0:.2f}".format(total_paid))
            print("current value:", "${0:.2f}".format(current_value))
            print("P/L per coin:","${0:.2f}".format(pl_percoin))
            print("Total P/L with coin:", "${0:.2f}".format(total_pl_coin))

            print("---------")

print("Total P/L for portfolio:", total_pl)