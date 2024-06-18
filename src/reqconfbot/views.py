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


class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(
        label="Green",
        style=ButtonStyle.green,
        custom_id="persistent_view:green",
    )
    async def green(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is green.", ephemeral=True)

    @ui.button(
        label="Red", style=ButtonStyle.red, custom_id="persistent_view:red"
    )
    async def red(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is red.", ephemeral=True)

    @ui.button(
        label="Grey", style=ButtonStyle.grey, custom_id="persistent_view:grey"
    )
    async def grey(self, button: Button, interaction: Interaction):
        await interaction.response.send_message("This is grey.", ephemeral=True)


# This is our actual board View.
class ViewTicTacToe(View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: list[ViewTicTacToe]
    x_id = -1
    o_id = 1
    tie_id = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.x_id
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner and is used by the TicTacToeButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.o_id
            elif value == -3:
                return self.x_id

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.o_id
            elif value == -3:
                return self.x_id

        # Check diagonals
        d = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if d == 3:
            return self.o_id
        elif d == -3:
            return self.x_id

        d = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if d == -3:
            return self.x_id
        elif d == 3:
            return self.o_id

        if all(i != 0 for row in self.board for i in row):
            return self.tie_id

        return None


class TicTacToeButton(Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    def __update(self, char: str, style: ButtonStyle, current: int) -> str:
        self.style = style
        self.label = char
        self.view.board[self.y][self.x] = current
        self.view.current_player = -current
        return f"Ход: {char}"

    async def callback(self, interaction: Interaction):
        assert self.view is not None

        v: ViewTicTacToe = self.view

        if v.board[self.y][self.x] != 0:
            return

        if v.current_player == v.x_id:
            content = self.__update("X", ButtonStyle.red, v.x_id)

        else:
            content = self.__update("O", ButtonStyle.blurple, v.o_id)

        self.disabled = True
        winner = v.check_board_winner()

        if winner is not None:
            if winner == v.x_id:
                content = "X won!"
            elif winner == v.o_id:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in v.children:
                child.disabled = True

            v.stop()

        await interaction.response.edit_message(content=content, view=v)
