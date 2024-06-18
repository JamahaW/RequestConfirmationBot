from __future__ import annotations
from __future__ import annotations

from discord import ButtonStyle
from discord import ButtonStyle
from discord import ButtonStyle
from discord import ButtonStyle
from discord import Interaction
from discord.ui import Button

from discord.ui import View


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
