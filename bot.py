import discord
import responses
import asyncio
import crypto

async def async_prices():
    return crypto.get_prices()

async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)
    
def run_discord_bot():
    TOKEN = "MTA3NTU3MzgzOTIwMDc5NjcwMg.GP5KIl.P71EQ5H2RS-Dq-Wp1iwQCguv1A0B-fIGpJFjSk"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    global curr_coin
    curr_coin = "ETH"

    async def update_status(symbol):
        global curr_coin
        curr_coin = symbol
        await client.wait_until_ready()
        while curr_coin == symbol:
            prices = await async_prices()
            coin_string = "> " + symbol + ": $" + str(prices[symbol])
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=coin_string))
            await asyncio.sleep(30)

    async def main(symbol):
        await client.wait_until_ready()
        client.loop.create_task(update_status(symbol))

    @client.event
    async def on_ready():
        await main("ETH")
        print(f" -- {client.user} NOW RUNNING -- ")


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" ({channel})')
        if len(user_message) > 0:
            if user_message.split()[0].lower() == "$watch" and len(user_message.split()) == 2:
                prices = await async_prices()
                if user_message.split()[1].upper() in prices:
                    await main(user_message.split()[1].upper())
                    await message.channel.send("now watching " + user_message.split()[1].upper())
                else:
                    user_message = user_message[1:]
                    await send_message(message, user_message)
            elif user_message[0] == "$":
                user_message = user_message[1:]
                await send_message(message, user_message)


    client.run(TOKEN)