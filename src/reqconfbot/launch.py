from typing import Any
from typing import Callable
from typing import Coroutine

from discord import ApplicationContext
from discord import ButtonStyle
from discord import Intents
from discord import Interaction
from discord import Member
from discord import Message
from discord import Option
from discord.ext.commands import Bot
from discord.ui import Button
from discord.ui import View


# USE PYCORD


def getConfig(path: str) -> dict[str, str]:
    import json
    with open(path, "r") as f:
        return json.load(f)


config = getConfig("A:/Program/Python3/RequestConfirmationBot/env.json")

bot = Bot(config["prefix"], intents=(Intents.default().all()))


@bot.event
async def on_ready():
    print(f"{bot.user.name} запустился и готов к работе!")


@bot.event
async def on_message(message: Message):
    if message.author.bot:
        return

    print(f'Получено сообщение! Текст: {message.content}, Сервер: {message.guild}')


def createButton(name: str, style: ButtonStyle, func: Callable[[Interaction], Coroutine[Any, Any, None]]) -> Button:
    b = Button(label=name, style=style)
    b.callback = func
    return b


@bot.slash_command(name='create_button', description='Создает зеленую кнопку')
async def create_button_command(context: ApplicationContext):
    async def button_callback(i: Interaction):
        await i.message.edit(content=f"{i.message.content}\n{i.user.name}")

    view = View(
        createButton("Зелёный", ButtonStyle.green, button_callback),
        createButton("Блурпул", ButtonStyle.blurple, button_callback),
        createButton("Красный", ButtonStyle.red, button_callback),
        timeout=None
    )

    await context.respond(view=view)


@bot.slash_command(name='test_slash_command')
async def __test(
        ctx,
        number: Option(int, description='Число в диапазоне от 1 до 10', required=True, min_value=1, max_value=10),
        member: Option(Member, description='Любой участник сервера', required=True),
        choice: Option(str, description='Выберите пункт из списка', required=True, choices=['Банан', 'Яблоко', 'Апельсин']),
        text: Option(str, description='Текст из нескольких слов', required=False, default=''),
        boolean: Option(bool, description='True или False', required=False, default=False)
):
    await ctx.delete()

    for argument in (number, boolean, member, text, choice):
        print(f'{argument} ({type(argument).__name__})\n')


@bot.slash_command(name='test', description='Отвечает "Успешный тест!"')
async def __test(ctx):
    await ctx.respond('Успешный тест!')


if __name__ == '__main__':
    print("Request Confirmation bot")
    bot.run(token=config['token'])
