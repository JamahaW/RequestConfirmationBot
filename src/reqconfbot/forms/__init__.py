from discord.ui import InputText
from discord.ui import Modal


class ModalTextBuilder(Modal):

    def add(self, inputText: InputText) -> InputText:
        self.add_item(inputText)
        return inputText
