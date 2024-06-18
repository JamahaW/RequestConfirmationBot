from typing import Optional

from discord import ButtonStyle
from discord import ComponentType
from discord import Interaction
from discord import SelectOption
from discord import ui
from discord.ui import Button
from discord.ui import Select
from discord.ui import View


class TestViewButtons2(View):

    @ui.button(label="Click me!", style=ButtonStyle.green, emoji="😎")
    async def click_me(self, _, interaction):
        await interaction.response.send_message("You clicked the button!")

    @ui.button(label="ban makoto", style=ButtonStyle.red)
    async def makoto_ban(self, _, interaction: Interaction):
        await interaction.response.send_message(
            "https://sun9-78.userapi.com/impf/3zOKwZaRpDi-FcQQPpUN0BaNMQIMX6g4uaAmWg/y61Uk1-U53Y.jpg?size=604x537&quality=96&sign=4b74013a10c9fd229cc6546f0941444a&type=album")


class TestViewSelectMenu(View):

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


class ConfirmView(View):

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


class CounterView(View):
    @ui.button(label="0", style=ButtonStyle.red)
    async def count(self, button: Button, interaction: Interaction):
        if (number := int(button.label) if button.label else 0) == 10:
            button.style = ButtonStyle.green
            button.disabled = True

        button.label = str(number + 1)

        await interaction.response.edit_message(view=self)


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

        v: TicTacToeView = self.view

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


# This is our actual board View.
class TicTacToeView(View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: list[TicTacToeButton]
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

        # Our board is made up of 3 by 3 TicTacToeButtons.
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
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
