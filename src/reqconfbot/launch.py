import random

from discord import Intents, Message
from discord.ext.commands import Bot


def getConfig(path: str) -> dict[str, str]:
    import json
    with open(path, "r") as f:
        return json.load(f)


config = getConfig("A:/Program/Python3/RequestConfirmationBot/env.json")

bot = Bot(config["prefix"], intents=(Intents.default().all()))


def getMessageInfo(msg: Message) -> str:
    return f"{msg.author}: {msg.content}"


# @bot.event
# async def on_message(ctx: Message):
#     if ctx.author != bot.user:
#         await ctx.reply(getMessageInfo(ctx))
#

@bot.command()
async def rand(ctx, *arg):
    await ctx.reply(random.randint(0, 100))


@bot.command()
async def sq(ctx, *args):
    x = int(args[0])
    await ctx.reply(f"{x}*{x} = {x * x}")


if __name__ == '__main__':
    print("Request Confirmation bot")
    bot.run(token=config['token'])
