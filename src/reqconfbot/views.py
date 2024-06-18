from __future__ import annotations

from typing import Optional

from discord import ButtonStyle
from discord import ComponentType
from discord import Interaction
from discord import SelectOption
from discord import ui
from discord.ui import Button
from discord.ui import Select
from discord.ui import View

from reqconfbot.buttons import CounterButton


class ViewTestButtons(View):

    @ui.button(label="Click me!", style=ButtonStyle.green, emoji="😎")
    async def click_me(self, _, interaction):
        await interaction.response.send_message("You clicked the button!")

    @ui.button(label="ban makoto", style=ButtonStyle.red)
    async def makoto_ban(self, _, interaction: Interaction):
        await interaction.response.send_message(
            "https://sun9-78.userapi.com/impf/3zOKwZaRpDi-FcQQPpUN0BaNMQIMX6g4uaAmWg/y61Uk1-U53Y.jpg?size=604x537&quality=96&sign=4b74013a10c9fd229cc6546f0941444a&type=album")


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


class ViewConfirm(View):

    def __init__(self):
        super().__init__()
        self.confirmed: Optional[bool] = None

    def __quit(self, status: bool, button: Button):
        self.confirmed = status
        button.label = f"|>{button.label}<|"
        button.disabled = True
        self.stop()

    @ui.button(label="Подтвердить", style=ButtonStyle.green)
    async def confirm(self, button: Button, interaction: Interaction):
        self.__quit(True, button)

    @ui.button(label="Отмена", style=ButtonStyle.danger)
    async def deny(self, button: Button, interaction: Interaction):
        self.__quit(False, button)


class ViewFavoriteColorVote(View):

    def __init__(self):
        super().__init__(timeout=None)

        colors = (
            ButtonStyle.red,
            ButtonStyle.green,
            ButtonStyle.gray,
            ButtonStyle.blurple
        )

        for color in colors:
            self.add_item(CounterButton(color.__str__(), style=color, custom_id=f"ViewFavoriteColorVote:{color}"))


class ViewExamplePersistent(View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Green", style=ButtonStyle.green, custom_id="persistent_view:green", )
    async def green(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is green.", ephemeral=True)

    @ui.button(label="Red", style=ButtonStyle.red, custom_id="persistent_view:red")
    async def red(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is red.", ephemeral=True)

    @ui.button(label="Grey", style=ButtonStyle.grey, custom_id="persistent_view:grey")
    async def grey(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is grey.", ephemeral=True)
