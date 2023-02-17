# uses livecoinwatch api

import requests
import json
  
url = "https://api.livecoinwatch.com/coins/list"
  
payload = json.dumps({
  "currency": "USD",
  "sort": "rank",
  "order": "ascending",
  "offset": 0,
  "limit": 25,
  "meta": False
})

headers = {
  "content-type": "application/json",
  "x-api-key": "d0300da2-374f-4502-843a-a18eaea5694b"
}
  
# returns prices
def get_prices():
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    prices = {}
    for r in response_json:
        prices[r["code"]] = "%.2f" % r["rate"]
    return prices

# returns market caps
def get_market_cap():
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    cap = {}
    for r in response_json:
        cap[r["code"]] = r["cap"]
    return cap

# returns daily percent change
def get_daily_change():
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    daily_change = {}
    for r in response_json:
        last_price = r["rate"] / r["delta"]["day"]
        daily_change[r["code"]] = "%.2f" % (((r["rate"] - last_price) / last_price) * 100)
    return daily_change

# returns info on specific crypto
def get_info(symbol):
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    info = {}
    for r in response_json:
        if r["code"] == symbol.upper():
            info["price"] = "%.2f" % r["rate"]
            info["mcap"] = r["cap"]
            last_price = r["rate"] / r["delta"]["day"]
            info["daily"] = "%.2f" % (((r["rate"] - last_price) / last_price) * 100)
            return info