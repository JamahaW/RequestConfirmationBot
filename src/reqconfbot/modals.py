from discord import Color
from discord import Embed
from discord import EmbedField
from discord import InputTextStyle
from discord import Interaction
from discord.ui import InputText
from discord.ui import Modal


class __ModalTextBuilder(Modal):

    def add(self, inputText: InputText) -> InputText:
        self.add_item(inputText)
        return inputText


class ModalFormSetup(__ModalTextBuilder):

    def __init__(self):
        super().__init__(title="Создать новое сообщение отправки заявок")

        self.autor = self.add(InputText(
            label="Автор",
            placeholder="Команда любителей занавесок",
            min_length=4,
            max_length=32,
            style=InputTextStyle.singleline
        ))

        self.thumbnail_url = self.add(InputText(
            label="Ссылка на эскиз",
            placeholder="Изображение вставленное в правом верхнем углу",
            style=InputTextStyle.short,
            required=False
        ))

        self.theme = self.add(InputText(
            label="Тема заявок",
            placeholder="Заявки на ...",
            min_length=8,
            max_length=40,
            style=InputTextStyle.singleline
        ))

        self.description = self.add(InputText(
            label="Описание",
            placeholder="В этом поле поддерживаемся MarkDown",
            min_length=20,
            max_length=500,
            style=InputTextStyle.long
        ))

        self.banner_url = self.add(InputText(
            label="ссылка на изображение баннера",
            placeholder="Изображение встроенное внизу",
            style=InputTextStyle.short,
            required=False
        ))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title=self.theme.value,
            color=Color.blurple(),
        )
        embed.set_author(name=self.autor.value)
        embed.set_thumbnail(url=self.thumbnail_url.value)
        embed.add_field(name="Описание", value=self.description.value, inline=False)
        embed.set_image(url=self.banner_url.value)

        await interaction.response.send_message(embed=embed)


class TestModal(__ModalTextBuilder):

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
