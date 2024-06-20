from discord import Color
from discord import Embed
from discord import EmbedField
from discord import InputTextStyle
from discord import Interaction
from discord.ui import InputText
from discord.ui import Modal


class ModalTextBuilder(Modal):

    def add(self, inputText: InputText) -> InputText:
        self.add_item(inputText)
        return inputText


class TestModal(ModalTextBuilder):

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

        embed = Embed(
            title="Данные пользователя",
            color=Color.red(),
            fields=list(
                EmbedField(c.label, c.value, False)
                for c in self.children
            )
        )

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
