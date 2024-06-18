from discord import ButtonStyle
from discord import Interaction
from discord.ui import Button


class CounterButton(Button):
    def __init__(self, label: str = None, end: int = None):
        self.__end = end
        self.__label_text = label
        self.__count: int = 0
        super().__init__(style=ButtonStyle.blurple, label=self.calculateLabel(), custom_id="counter_button")

    def calculateLabel(self) -> str:
        if self.__label_text is None:
            return f"{self.__count}"

        return f"{self.__label_text}: {self.__count}"

    async def callback(self, interaction: Interaction):
        if self.__end is not None and self.__count >= self.__end:
            self.style = ButtonStyle.gray
            self.disabled = True

        else:
            self.__count += 1
            self.label = self.calculateLabel()

        await interaction.response.edit_message(view=self.view)
