from __future__ import annotations

from typing import Iterable
from typing import Optional

from discord import ButtonStyle
from discord import Color
from discord import Embed
from discord import EmbedAuthor
from discord import InputTextStyle
from discord import Interaction
from discord import SelectOption
from discord import ui
from discord.ui import Button
from discord.ui import InputText
from discord.ui import Select
from discord.ui import View

from reqconfbot.modals import ModalTextBuilder


class ModalFormSetup(ModalTextBuilder):

    def __init__(self):
        super().__init__(title="Создать новое сообщение отправки заявок")

        self.author = self.add(InputText(
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
        await interaction.response.send_message(
            embed=EmbedForm(
                self.author.value,
                self.thumbnail_url.value,
                self.description.value,
                self.banner_url.value,
                title=self.theme.value,
                color=Color.blurple()
            ),
            view=ViewSendModalRequest()
        )


class EmbedForm(Embed):

    def __init__(self, author: str, thumbnail: str, description: str, image: str, **kwargs):
        super().__init__(
            author=EmbedAuthor(author),
            image=image,
            thumbnail=thumbnail, **kwargs
        )
        self.add_field(name="Описание", value=description, inline=False)


class ViewSendModalRequest(View):

    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Заполнить", style=ButtonStyle.green, custom_id="ModalFormSetup:view:button")
    async def send_modal(self, _, interaction: Interaction):
        await interaction.response.send_modal(modal=ModalNethexForm())


class ModalNethexForm(ModalTextBuilder):

    def __init__(self):
        super().__init__(title="Заявка")

        self.minecraft_nickname = self.add(InputText(
            style=InputTextStyle.singleline,
            label="Ваш ник-нейм в майнкрафт",
            placeholder="(Без пробелов, только латинские буквы и '_')",
            min_length=3,
            max_length=16
        ))

        self.played_servers = self.add(InputText(
            style=InputTextStyle.multiline,
            label="На каких серверах подобного жанра вы играли?",
            placeholder="Перечислите несколько",
            min_length=10,
            max_length=200
        ))

        self.user_plannings = self.add(InputText(
            style=InputTextStyle.multiline,
            label="Чем планируете заниматься на сервере?",
            placeholder="Сформулируйте несколько целей или занятий",
            min_length=50,
            max_length=500
        ))

        self.etc = self.add(InputText(
            style=InputTextStyle.multiline,
            label="Дополнительная информация",
            max_length=300,
            required=False
        ))

    async def callback(self, interaction: Interaction):
        await interaction.respond("Заполните этот опрос, чтобы завершить заявку", ephemeral=True, view=ViewUserVote(self, interaction))


class SelectUserString(Select["ViewUserVote"]):

    def __init__(self, select: UserSelect, placeholder: str, options: Iterable[SelectOption]):
        super().__init__(
            placeholder=placeholder,
            options=list(options)
        )
        self.select = select

    async def callback(self, interaction: Interaction):
        self.select.value = interaction.data["values"][0]
        if self.view.selectDone():
            await self.view.updateParent(button_disable=False)

        await interaction.response.defer(ephemeral=True)


class ButtonFormSend(Button["ViewUserVote"]):

    def __init__(self, label: str):
        super().__init__(label=label, style=ButtonStyle.green, disabled=True)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        await interaction.respond("Ваша заявка была отправлена", ephemeral=True)
        await self.view.updateParent(button_disable=True)
        print("заявка")


class UserSelect:
    def __init__(self):
        self.value: Optional[str] = None


class ViewUserVote(View):

    async def updateParent(self, button_disable: bool) -> None:
        self.button.disabled = button_disable
        await self.parent_interation.edit(view=self)

    def selectDone(self) -> bool:
        return None not in (self.select_known.value, self.select_client.value)

    def __init__(self, modal: ModalNethexForm, parent_interaction: Interaction) -> None:
        super().__init__()
        self.modal = modal
        self.parent_interation = parent_interaction

        self.select_client = UserSelect()
        self.select_known = UserSelect()

        self.add_item(SelectUserString(
            self.select_known,
            "Откуда вы узнали о нашем сервере?",
            (
                SelectOption(label="Реклама ВКонтакте"),
                SelectOption(label="Реклама на сторонних сервисах"),
                SelectOption(label="Узнал от друзей/компании"),
            )
        ))

        self.add_item(SelectUserString(
            self.select_client,
            "Какой клиент вы используете?",
            (
                SelectOption(label="Лицензионный"),
                SelectOption(label="Пиратский"),
            )
        ))

        self.button = ButtonFormSend("Отправить заявку на проверку")
        self.add_item(self.button)
