from discord import ApplicationContext
from discord import ButtonStyle
from discord import ComponentType
from discord import Intents
from discord import Interaction
from discord import Member
from discord import Message
from discord import Option
from discord import SelectOption
from discord import ui
from discord.ext.commands import Bot
from discord.ui import Select


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


@bot.slash_command()
async def button_my_view(ctx):
    class MyView(ui.View):
        @ui.button(label="Click me!", style=ButtonStyle.green, emoji="😎")
        async def click_me(self, _, interaction):
            await interaction.response.send_message("You clicked the button!")

        @ui.button(label="ban makoto", style=ButtonStyle.red)
        async def makoto_ban(self, _, interaction: Interaction):
            await interaction.response.send_message("makoto bam")

    await ctx.respond("This is a button!", view=MyView())


@bot.slash_command()
async def select_menu_demo(context: ApplicationContext):
    class ViewSelectMenu(ui.View):
        @ui.button(label="Click", style=ButtonStyle.green)
        async def click_me(self, _, interaction):
            await interaction.response.send_message("select")

        @ui.select(ComponentType.string_select, options=[
            SelectOption(label='Яблоко', emoji='🍏', default=True),
            SelectOption(label='Банан', emoji='🍌'),
            SelectOption(label='Апельсин', emoji='🍊'),
        ])
        async def select_callback(self, _: Select, interaction: Interaction):
            await interaction.response.defer()
            await interaction.message.edit(content=f'{interaction.user.name} выбрал {interaction.data["values"][0]}')

    await context.respond("view", view=ViewSelectMenu())


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


if __name__ == '__main__':
    print("Request Confirmation bot")
    bot.run(token=config['token'])
