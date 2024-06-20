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


"""
* Ваш будущий ник-нейм внутри сервера
* На каких серверах подоброго жанра вы играли?
* Чем планируете заниматься на сервере первым делом или в будущем по развитию?
* Вы можете дополнить текст для того Мастера, который будет проверять вашу заявку, дополнить её или расписать поподробнее если что-то не поместилось.
"""


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


"""
Откуда вы узнали о нашем сервере?
 - Реклама ВКонтакте
 - Реклама на сторонних сервисах
 - Узнал от друзей/компании

Какой клиент вы используете?
 - Лицензионный (куплена лицензия майнкрафта)
 - Тлаунчер и другие пиратские лаунчеры
"""


class ViewSelectMenuTest(View):

    @ui.button(label="Click", style=ButtonStyle.green)
    async def click_me(self, _, interaction):
        await interaction.response.send_message("select")

    @ui.select(options=[
        SelectOption(label='Яблоко', emoji='🍏'),
        SelectOption(label='Банан', emoji='🍌'),
        SelectOption(label='Апельсин', emoji='🍊'),
    ])
    async def select_callback(self, _: Select, interaction: Interaction):
        await interaction.response.defer()
        await interaction.message.edit(content=f'{interaction.user.name} выбрал {interaction.data["values"][0]}')


class ViewUserVote(View):

    def __init__(self, modal: ModalNethexForm, parent_interaction: Interaction) -> None:
        super().__init__()
        self.modal = modal
        self.parent_interation = parent_interaction

    @ui.button(label="Отправить заявку на проверку", style=ButtonStyle.green)
    async def send_form(self, button: Button, interaction: Interaction):
        button.disabled = True
        await self.parent_interation.edit(view=self)
        await interaction.respond("Ваша заявка была отправлена", ephemeral=True)
