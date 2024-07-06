from __future__ import annotations

import re
from typing import Final

from discord import ButtonStyle
from discord import Color
from discord import Embed
from discord import EmbedAuthor
from discord import EmbedFooter
from discord import InputTextStyle
from discord import Interaction
from discord import Member
from discord import User
from discord import ui
from discord.ui import Button
from discord.ui import InputText
from discord.ui import Modal
from discord.ui import View

from reqconfbot.jsondatabase import ServerData
from reqconfbot.jsondatabase import ServerJSONDatabase


class ModalTextBuilder(Modal):

    def add(self, inputText: InputText) -> InputText:
        self.add_item(inputText)
        return inputText


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
            max_length=1000,
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
            embed=Embed(
                author=EmbedAuthor(self.author.value),
                thumbnail=self.thumbnail_url.value,
                description=self.description.value,
                image=self.banner_url.value,
                title=self.theme.value,
                color=Color.blurple()
            ),
            view=ViewSendModalRequest()
        )


class ViewSendModalRequest(View):
    server_database: ServerJSONDatabase = None

    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Заполнить", style=ButtonStyle.green, custom_id="ModalFormSetup:view:button")
    async def send_modal(self, _, interaction: Interaction):
        # interaction.response: InteractionResponse
        await interaction.response.send_modal(
            ModalNethexForm(self.__class__.server_database.get(interaction.guild_id))
        )


class ModalNethexForm(ModalTextBuilder):
    MINECRAFT_NICKNAME_PATTERN = r'^[a-zA-Z0-9_]+$'

    def __init__(self, server_data: ServerData):
        super().__init__(title="Заявка")
        self.server_data = server_data

        self.minecraft_nickname = self.add(InputText(
            style=InputTextStyle.singleline,
            label="Ваш ник в майнкрафт",
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

    @classmethod
    def minecraftNicknameCheck(cls, nickname: str) -> bool:
        return re.match(cls.MINECRAFT_NICKNAME_PATTERN, nickname) is not None

    async def callback(self, interaction: Interaction):
        if not self.minecraftNicknameCheck(self.minecraft_nickname.value):
            await interaction.respond(f"`{self.minecraft_nickname.value}` - Такой ник не может быть использован в minecraft!")
            return

        embed = EmbedUserForm(interaction, self)
        await interaction.respond("Ваша заявка отправлена администрации и её копия вам в ЛС", ephemeral=True, embed=embed)
        await interaction.guild.get_channel(self.server_data.form_channel_id).send(embed=embed, view=ViewUserForm())
        await interaction.user.send(content="# Ваша заявка была отправлена, ожидайте подтверждения", embed=embed)


class EmbedUserForm(Embed):
    FOOTER_VALUES_SEPARATOR: Final[str] = ";"

    @classmethod
    def dumpInFooter(cls, user: User, nickname: str) -> EmbedFooter:
        return EmbedFooter(text=f"{user.id}{cls.FOOTER_VALUES_SEPARATOR}{nickname}")

    @classmethod
    def parseFromFooter(cls, footer: EmbedFooter) -> tuple[int, str]:
        user_id, nickname = footer.text.split(cls.FOOTER_VALUES_SEPARATOR)
        return int(user_id), nickname

    def __init__(self, parent_interaction: Interaction, modal: ModalNethexForm):
        user = parent_interaction.user

        super().__init__(
            title=f"Заявка от {user.name}",
            color=Color.gold(),
            author=EmbedAuthor(name=user.display_name, icon_url=user.display_avatar.url),
            footer=self.dumpInFooter(user, modal.minecraft_nickname.value),
            thumbnail=user.display_avatar.url
        )

        self.add_field(name="Никнейм", value=modal.minecraft_nickname.value, inline=True)
        self.add_field(name="Играл на серверах:", value=modal.played_servers.value, inline=False)
        self.add_field(name="Планы на сезон", value=modal.user_plannings.value, inline=False)

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

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        embed.add_field(name="Сервер", value=interaction.guild.name, inline=True)
        await member.send(embed=embed)

        server = self.view.server_database.get(interaction.guild_id)

        cmds = server.getFormattedCommand(nickname, member.id)

        for cmd in cmds:
            await interaction.guild.get_channel(server.commands_send_channel_id).send(content=cmd)

    async def callback(self, interaction: Interaction):
        self.view.disable_all_items()

        e = interaction.message.embeds[0]
        member_id, nickname = EmbedUserForm.parseFromFooter(e.footer)
        member = interaction.guild.get_member(member_id)

        embed = Embed(
            color=self.color,
            title=f"{self.status} ({e.author.name})",
            thumbnail=e.thumbnail,
            fields=e.fields
        )

        await self.memberProcess(interaction, member, embed, nickname)
        await interaction.edit(view=self.view, embed=embed)


class ButtonUserFormDeny(ButtonUserForm):

    def __init__(self):
        super().__init__(label="Отклонить", style=ButtonStyle.red, color=Color.red(), status="Отклонён")

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        await interaction.response.send_modal(ModalUserFormDeny(member, embed, nickname))


class ModalUserFormDeny(ModalTextBuilder):

    def __init__(self, member: Member, embed: Embed, nickname: str):
        super().__init__(title=f"отказ {nickname}")

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
    server_database: ServerJSONDatabase = None

    def __init__(self):
        super().__init__(
            ButtonUserForm(label="Принять", style=ButtonStyle.green, color=Color.green(), status="Принят"),
            ButtonUserFormDeny(),
            timeout=None
        )
