from discord import ApplicationContext
from discord import ButtonStyle
from discord import Color
from discord import ComponentType
from discord import Embed
from discord import InputTextStyle
from discord import Intents
from discord import Interaction
from discord import Member
from discord import Message
from discord import Option
from discord import SelectOption
from discord import ui
from discord.ext.commands import Bot
from discord.ui import InputText
from discord.ui import Modal
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
            SelectOption(label='Яблоко', emoji='🍏'),
            SelectOption(label='Банан', emoji='🍌'),
            SelectOption(label='Апельсин', emoji='🍊'),
        ])
        async def select_callback(self, _: Select, interaction: Interaction):
            await interaction.response.defer()
            await interaction.message.edit(content=f'{interaction.user.name} выбрал {interaction.data["values"][0]}')

    await context.respond("view", view=ViewSelectMenu())


@bot.slash_command()
async def test_form(context: ApplicationContext):
    class TestModal(Modal):

        def add(self, inputText: InputText) -> InputText:
            self.add_item(inputText)
            return inputText

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.name = self.add(InputText(
                label="ввод имя",
                placeholder="Ваше имя",
                min_length=3,
                max_length=20,
                style=InputTextStyle.singleline
            ))

            self.desc = self.add(InputText(
                label="ввод описание",
                placeholder="Описание",
                min_length=20,
                max_length=2000,
                style=InputTextStyle.long
            ))

            self.age = self.add(InputText(
                label="ввод возраст (число)",
                placeholder="целое положительное число",
                style=InputTextStyle.short
            ))

        async def send(self, interaction: Interaction, message: str):
            text = f"## Заявка от {interaction.user.name}\n{message}"

            embed = Embed(title="Данные пользователя", color=Color.red(), type="rich")

            for field in self.children:
                embed.add_field(name=field.label, value=field.value, inline=False)

            await interaction.response.send_message(text, embed=embed)

        async def deny(self, interaction: Interaction, error_msg: str):
            await self.send(interaction, f"Ошибка заполнения формы: {error_msg}")

        async def callback(self, interaction: Interaction):
            try:
                if (age := int(self.age.value)) < 0:
                    await self.deny(interaction, f"Недействительный возраст ({age})")
                    return

            except ValueError as e:
                await self.deny(interaction, f"Возраст не был числом ({e})")

            await self.send(interaction, "Отправлена на рассмотрение администрации")

    await context.send_modal(TestModal(title="Заявка тест"))


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
