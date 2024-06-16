import random

from discord import Intents, Message, Member, Attachment
from discord.ext import commands
from discord.ext.commands import Bot, Greedy, FlagConverter, BadArgument


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


class BanFlags(FlagConverter):
    member: Member
    reason: str
    days: int = 1


@bot.command()
async def info(ctx, *, member: Member):
    """Tells you some info about the member."""
    msg = f'{member} joined on {member.joined_at} and has {member.roles} roles.'
    await ctx.send(msg)


@info.error
async def info_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send('I could not find that member...')


# @bot.command()
# async def haban(ctx, *, flags: BanFlags):
#     plural = f'{flags.days} days' if flags.days != 1 else f'{flags.days} day'
#     await ctx.send(f'Banned {flags.member} for {flags.reason!r} (deleted {plural} worth of messages)')


@bot.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, code):
    """A bad example of an eval command"""
    await ctx.send(eval(code))


if __name__ == '__main__':
    print("Request Confirmation bot")
    bot.run(token=config['token'])
