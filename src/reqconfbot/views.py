from discord import ButtonStyle
from discord import ComponentType
from discord import Interaction
from discord import SelectOption
from discord import ui
from discord.ui import Select


class TestViewButtons2(ui.View):

    @ui.button(label="Click me!", style=ButtonStyle.green, emoji="😎")
    async def click_me(self, _, interaction):
        await interaction.response.send_message("You clicked the button!")

    @ui.button(label="ban makoto", style=ButtonStyle.red)
    async def makoto_ban(self, _, interaction: Interaction):
        await interaction.response.send_message("makoto bam")


class TestViewSelectMenu(ui.View):

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
