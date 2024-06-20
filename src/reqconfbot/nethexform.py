from __future__ import annotations

from typing import Iterable
from typing import Optional

from discord import ButtonStyle
from discord import Color
from discord import Embed
from discord import EmbedAuthor
from discord import EmbedFooter
from discord import InputTextStyle
from discord import Interaction
from discord import Member
from discord import SelectOption
from discord import ui
from discord.ui import Button
from discord.ui import InputText
from discord.ui import Select
from discord.ui import View

from reqconfbot.jsondatabase import ServerData
from reqconfbot.jsondatabase import ServerJSONDatabase
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
            embed=EmbedCreateForm(
                self.author.value,
                self.thumbnail_url.value,
                self.description.value,
                self.banner_url.value,
                title=self.theme.value,
                color=Color.blurple()
            ),
            view=ViewSendModalRequest()
        )


class EmbedCreateForm(Embed):

    def __init__(self, author: str, thumbnail: str, description: str, image: str, **kwargs):
        super().__init__(
            author=EmbedAuthor(author),
            image=image,
            thumbnail=thumbnail, **kwargs
        )
        self.add_field(name="Описание", value=description, inline=False)


class ViewSendModalRequest(View):
    server_database: ServerJSONDatabase = None

    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Заполнить", style=ButtonStyle.green, custom_id="ModalFormSetup:view:button")
    async def send_modal(self, _, interaction: Interaction):
        await interaction.response.send_modal(modal=ModalNethexForm(self.__class__.server_database.get(interaction.guild_id)))


class ModalNethexForm(ModalTextBuilder):

    def __init__(self, server_data: ServerData):
        super().__init__(title="Заявка")
        self.server_data = server_data

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
        await self.view.updateParent(button_disable=True)

        embed = EmbedUserForm(interaction, self.view)

        await interaction.respond("Ваша заявка отправлена администрации и вам в ЛС", ephemeral=True, embed=embed)
        await interaction.guild.get_channel(self.view.modal.server_data.form_channel_id).send(embed=embed, view=ViewUserForm())
        await interaction.user.send(embed=embed)


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

        self.button = ButtonFormSend("Отправить заявку")
        self.add_item(self.button)


class EmbedUserForm(Embed):
    def __init__(self, parent_interaction: Interaction, user_vote: ViewUserVote):
        user = parent_interaction.user

        super().__init__(
            title=f"Заявка от {user.name}",
            color=Color.gold(),
            author=EmbedAuthor(name=user.display_name, icon_url=user.display_avatar.url),
            footer=EmbedFooter(f"{user.id}"),
            thumbnail=user.display_avatar.url
        )

        modal = user_vote.modal

        self.add_field(name="Никнейм", value=modal.minecraft_nickname.value, inline=True)
        self.add_field(name="Клиент", value=user_vote.select_client.value, inline=True)

        self.add_field(name="Узнал из", value=user_vote.select_known.value, inline=False)
        self.add_field(name="Играл на серверах:", value=modal.played_servers.value, inline=False)

        if modal.etc.value:
            self.add_field(name="Дополнительная информация", value=modal.etc.value, inline=False)


class ButtonUserForm(Button["ViewUserForm"]):

    def __init__(self, label: str, style: ButtonStyle, color: Color, status: str):
        super().__init__(
            label=label,
            custom_id=f"ButtonUserForm:{label}",
            style=style
        )

        self.status = status
        self.color = color

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed):
        await member.send(embed=embed)

    async def callback(self, interaction: Interaction):
        self.view.disable_all_items()

        e = interaction.message.embeds[0]
        member = interaction.guild.get_member(int(e.footer.text))

        embed = Embed(
            color=self.color,
            title=f"{self.status} ({e.author.name})",
            thumbnail=e.thumbnail
        )

        await self.memberProcess(interaction, member, embed)
        await interaction.edit(view=self.view, embed=embed)


class ButtonUserFormDeny(ButtonUserForm):

    def __init__(self):
        super().__init__(label="Отклонить", style=ButtonStyle.red, color=Color.red(), status="Отклонён")

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed):
        await interaction.response.send_modal(ModalUserFormDeny(member, embed))


class ModalUserFormDeny(ModalTextBuilder):

    def __init__(self, member: Member, embed: Embed):
        super().__init__(title="Указать причину отказа заявки")

        self.reason = self.add(InputText(
            style=InputTextStyle.singleline,
            value="Не подходишь",
            label="Причина",
            min_length=8,
            max_length=32
        ))

        self.member = member
        self.embed = embed

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.embed.add_field(name="Причина", value=self.reason.value, inline=False)
        await self.member.send(embed=self.embed)


class ViewUserForm(View):

    def __init__(self):
        super().__init__(
            ButtonUserForm(label="Принять", style=ButtonStyle.green, color=Color.green(), status="Принят"),
            ButtonUserFormDeny(),
            timeout=None
        )
