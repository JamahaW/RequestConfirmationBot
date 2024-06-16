import random

from discord import Intents, Message, Member, Attachment
from discord.ext.commands import Bot, Greedy, MemberConverter


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
async def rand(ctx):
    await ctx.reply(random.randint(0, 100))


@bot.command()
async def sq(ctx, x: int):
    await ctx.reply(f"{x}*{x} = {x * x}")


#
# class Slapper(commands.Converter):
#     async def convert(self, ctx, argument):
#         to_slap = random.choice(ctx.guild.members)
#         return f'{ctx.author} slapped {to_slap} because *{argument}*'
#

# @bot.command()
# async def slap(ctx, *, reason: Slapper):
#     await ctx.send(reason)

@bot.command()
async def slap(ctx, members: Greedy[Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send(f'{slapped} just got slapped for {reason}')


# @bot.command()
# async def upload(ctx, attachment: Attachment):
#     await ctx.send(f'You have uploaded <{attachment.url}>')


@bot.command()
async def upload(
        ctx,
        first: Attachment,
        remaining: Greedy[Attachment],
):
    files = [first.url]
    files.extend(f'{a.url}\n' for a in remaining)
    await ctx.send(f'You uploaded: {" ".join(files)}')


# class JoinDistance:
#     def __init__(self, joined, created):
#         self.joined = joined
#         self.created = created
#
#     def delta(self):
#         return self.joined - self.created

#
# class JoinDistanceConverter(MemberConverter):
#     async def convert(self, ctx, argument):
#         member = await super().convert(ctx, argument)
#         return JoinDistance(member.joined_at, member.created_at)
#

# @bot.command()
# async def delta(ctx, *, member: JoinDistanceConverter):
#     await ctx.send(f"days: {member.delta().days}")


if __name__ == '__main__':
    print("Request Confirmation bot")
    bot.run(token=config['token'])
