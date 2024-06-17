from typing import Any
from typing import Callable
from typing import Coroutine

import discord
from discord import ApplicationContext
from discord import ButtonStyle
from discord import Intents
from discord import Interaction
from discord import Member
from discord import Message
from discord import Option
from discord import SelectOption
from discord.ext.commands import Bot
from discord.ui import Button
from discord.ui import Select
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
        createButton("Красный", ButtonStyle.red, button_callback)
    )

    await context.respond(view=view)


class MyView(View):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=ButtonStyle.primary, emoji="😎")  # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")  # Send a message when the button is clicked


@bot.slash_command()  # Create a slash command
async def button_my_view(ctx):
    await ctx.respond("This is a button!", view=MyView())  # Send a message with our View class that contains the button


@bot.slash_command(name='create_select_menu', description='Создает выпадающий список', guild_ids=[830851544093163530])
async def create_button_command__(context: ApplicationContext):
    view = View()

    async def select_callback(interaction: Interaction):
        await interaction.message.edit(content=f'{interaction.user.name} выбрал {interaction.data["values"][0]}')

    select = Select(
        options=[
            SelectOption(label='Яблоко', emoji='🍏', default=True),
            SelectOption(label='Банан', emoji='🍌'),
            SelectOption(label='Апельсин', emoji='🍊'),
        ]
    )

    select.callback = select_callback
    view.add_item(select)

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
