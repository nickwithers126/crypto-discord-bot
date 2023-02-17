import random
import crypto

def get_response(message: str) -> str:

    p_message = message.lower()

    if p_message == "commands":
        return ("` ** NOTE - coins must be top 25 by market cap ** \n"
                "$watch [TICKER] - change current watched coin to TICKER\n"
                "$[TICKER] - display information for TICKER\n"
                "$prices - display prices for top 25 coins\n"
                "$24hr - display 24 hr percent change for top 25 coins\n"
                "$mcap - display market cap for top 25 coins\n`")

    if p_message == "prices":
        prices = crypto.get_prices()
        res = ""
        for key in prices:
            res = res + key + ": $" + prices[key] + "\n"
        return res

    if p_message == "mcap":
        mcap = crypto.get_market_cap()
        res = ""
        for key in mcap:
            res = res + key + ": $" + str(mcap[key]) + "\n"
        return res

    if p_message == "24hr":
        daily = crypto.get_daily_change()
        res = ""
        for key in daily:
            if float(daily[key]) < 0:
                res = res + key + ": -%" + str(abs(float(daily[key]))) + "\n"
            else:
                res = res + key + ": +%" + daily[key] + "\n"
        return res

    coins = crypto.get_prices()
    if p_message.upper() in coins:
        info = crypto.get_info(p_message)
        res = ""
        res += "price: $" + info["price"] + "\n"
        if float(info["daily"]) < 0:
            res += "24 hr change: -%" + str(abs(float(info["daily"]))) + "\n"
        else:
             res += "24 hr change: +%" + info["daily"] + "\n"
        res += "market cap: $" + str(info["mcap"])
        return res

    return "didn't get that. try typing `$commands`"