from __future__ import annotations

from discord import ButtonStyle
from discord import ComponentType
from discord import Interaction
from discord import SelectOption
from discord import ui
from discord.ui import Select
from discord.ui import View


class ViewSelectMenuTest(View):

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
