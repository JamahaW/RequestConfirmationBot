from __future__ import annotations

import re
from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import Optional

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

from reqconfbot.lang.nethex import NethexLang
from reqconfbot.lang.panelcreator import PanelCreatorLang


class ModalTextBuilder(Modal):

    def add(self, inputText: InputText) -> InputText:
        self.add_item(inputText)
        return inputText


class PanelCreatorLangEmbed(Embed):
    def __init__(self, createPanelModal: PanelCreatorLangModal):
        super().__init__(
            author=EmbedAuthor(createPanelModal.author.value),
            thumbnail=createPanelModal.thumbnail_url.value,
            description=createPanelModal.description.value,
            image=createPanelModal.banner_url.value,
            title=createPanelModal.theme.value,
            color=Color.gold()
        )


class PanelCreatorLangModal(ModalTextBuilder):

    def __init__(self):
        super().__init__(title=PanelCreatorLang.MODAL_TITLE)

        self.author = self.add(InputText(
            label=PanelCreatorLang.MODAL_AUTHOR_LABEL,
            placeholder=PanelCreatorLang.MODAL_AUTHOR_PLACEHOLDER,
            min_length=4,
            max_length=32,
            style=InputTextStyle.singleline
        ))

        self.thumbnail_url = self.add(InputText(
            label=PanelCreatorLang.MODAL_THUMBNAIL_URL_LABEL,
            placeholder=PanelCreatorLang.MODAL_THUMBNAIL_URL_PLACEHOLDER,
            style=InputTextStyle.short,
            required=False
        ))

        self.theme = self.add(InputText(
            label=PanelCreatorLang.MODAL_THEME_LABEL,
            placeholder=PanelCreatorLang.MODAL_THEME_PLACEHOLDER,
            min_length=8,
            max_length=40,
            style=InputTextStyle.singleline
        ))

        self.description = self.add(InputText(
            label=PanelCreatorLang.MODAL_DESCRIPTION_LABEL,
            placeholder=PanelCreatorLang.MODAL_DESCRIPTION_PLACEHOLDER,
            min_length=20,
            max_length=1000,
            style=InputTextStyle.long
        ))

        self.banner_url = self.add(InputText(
            label=PanelCreatorLang.MODAL_BANNER_URL_LABEL,
            placeholder=PanelCreatorLang.MODAL_BANNER_URL_PLACEHOLDER,
            style=InputTextStyle.short,
            required=False
        ))

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(
            embed=PanelCreatorLangEmbed(self),
            view=NethexPanelCreatorLangView()
        )
        await interaction.respond("успешно отправлено", ephemeral=True)


class NethexFormEmbed(Embed):
    FOOTER_VALUES_SEPARATOR: ClassVar[str] = ";"

    @classmethod
    def dumpInFooter(cls, user: User, nickname: str) -> EmbedFooter:
        return EmbedFooter(text=f"{user.id}{cls.FOOTER_VALUES_SEPARATOR}{nickname}")

    @classmethod
    def parseFromFooter(cls, footer: EmbedFooter) -> tuple[int, str]:
        user_id, nickname = footer.text.split(cls.FOOTER_VALUES_SEPARATOR)
        return int(user_id), nickname

    def __init__(self, parent_interaction: Interaction, modal: NethexFormModal):
        user = parent_interaction.user
        super().__init__(
            title=NethexLang.EMBED_TITLE.format(user.name),
            color=Color.gold(),
            author=EmbedAuthor(name=user.display_name, icon_url=user.display_avatar.url),
            footer=self.dumpInFooter(user, modal.minecraft_nickname.value),
            thumbnail=user.display_avatar.url
        )

        self.add_field(name=NethexLang.EMBED_FIELD_NAME, value=modal.minecraft_nickname.value, inline=True)
        self.add_field(name=NethexLang.EMBED_FIELD_SERVERS_PLAYED_ON, value=modal.played_servers.value, inline=False)
        self.add_field(name=NethexLang.EMBED_FIELD_SEASON_PLANNINGS, value=modal.user_plannings.value, inline=False)

        if modal.etc.value:
            self.add_field(name=NethexLang.EMBED_FIELD_INFO, value=modal.etc.value, inline=False)


class NethexFormButton(Button["ViewUserForm"], ABC):

    def __init__(self, label: str, style: ButtonStyle, color: Color, status: str):
        super().__init__(label=label, custom_id=f"ButtonUserForm:{label}", style=style)
        self.status = status
        self.embed_status_color = color

    @abstractmethod
    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        """Поведение кнопки формы"""

    async def callback(self, interaction: Interaction):
        self.view.disable_all_items()
        embed = self.updateEmbed(interaction.message.embeds[0])
        member, nickname = await self.getMemberAndNickname(embed, interaction)
        await self.memberProcess(interaction, member, embed, nickname)
        await interaction.edit(view=self.view, embed=embed)

    def updateEmbed(self, e: Embed) -> Embed:
        return Embed(
            color=self.embed_status_color,
            title=f"{self.status} ({e.author.name})",
            fields=e.fields,
            footer=e.footer
        )

    @staticmethod
    async def getMemberAndNickname(embed, interaction):
        member_id, nickname = NethexFormEmbed.parseFromFooter(embed.footer)
        return (
            interaction.guild.get_member(member_id),
            nickname
        )


class NethexFormApplyButtonButton(NethexFormButton):
    def __init__(self):
        super().__init__(label=NethexLang.APPLY_BUTTON_LABEL, style=ButtonStyle.green, color=Color.green(), status=NethexLang.APPLY_BUTTON_STATUS)

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        await member.send(embed=embed)
        await self.sendCommands(interaction, member, nickname)

    @staticmethod
    async def sendCommands(interaction, member, nickname):
        from reqconfbot.cogs.nethex import NethexCog
        server_data = NethexCog.database.get(interaction.guild_id)
        for cmd in server_data.getFormattedCommands(nickname, member.id):
            await interaction.guild.get_channel(server_data.minecraft_commands_channel_id).send(content=cmd)


class NethexFormView(View):

    def __init__(self):
        super().__init__(NethexFormApplyButtonButton(), NethexFormDenyButtonButton(), timeout=None)


class NethexFormDenyModal(ModalTextBuilder):

    def __init__(self, member: Member, embed: Embed, nickname: str):
        super().__init__(title=NethexLang.DENY_MODAL_TITLE.format(nickname))

        self.reason = self.add(InputText(
            style=InputTextStyle.singleline,
            value=NethexLang.DENY_MODAL_VALUE,
            label=NethexLang.DENY_MODAL_LABEL,
            min_length=8,
            max_length=32
        ))

        self.member = member
        self.embed = embed

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.embed.add_field(name=NethexLang.DENY_EMBED_FIELD_DENY_REASON, value=self.reason.value, inline=False)
        await interaction.message.edit(embed=self.embed)
        await self.member.send(embed=self.embed)


class NethexFormDenyButtonButton(NethexFormButton):

    def __init__(self):
        super().__init__(label=NethexLang.DENY_BUTTON_TITLE, style=ButtonStyle.red, color=Color.red(), status=NethexLang.DENY_BUTTON_STATUS)

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        await interaction.response.send_modal(NethexFormDenyModal(member, embed, nickname))


class NethexFormModal(ModalTextBuilder):
    MINECRAFT_NICKNAME_REGEX: ClassVar[str] = r'^[a-zA-Z0-9_]+$'

    def __init__(self, guild_id: int):
        super().__init__(title=NethexLang.MODAL_TITLE)
        self.guild_id = guild_id

        self.minecraft_nickname = self.add(InputText(
            style=InputTextStyle.singleline,
            label=NethexLang.MODAL_MINECRAFT_NICKNAME_LABEL,
            placeholder=NethexLang.MODAL_MINECRAFT_NICKNAME_PLACEHOLDER,
            min_length=3,
            max_length=16
        ))

        self.played_servers = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexLang.MODAL_PLAYED_SERVERS_LABEL,
            placeholder=NethexLang.MODAL_PLAYER_SERVERS_PLACEHOLDER,
            min_length=10,
            max_length=200
        ))

        self.user_plannings = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexLang.MODAL_PLANNINGS_LABEL,
            placeholder=NethexLang.MODAL_PLANNINGS_PLACEHOLDER,
            min_length=50,
            max_length=500
        ))

        self.etc = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexLang.MODAL_INFO_LABEL,
            max_length=300,
            required=False
        ))

    @classmethod
    def checkNickname(cls, nickname: str) -> bool:
        return re.match(cls.MINECRAFT_NICKNAME_REGEX, nickname) is not None

    async def callback(self, interaction: Interaction):
        if not self.checkNickname(self.minecraft_nickname.value):
            await interaction.respond(NethexLang.MODAL_MINECRAFT_NICKNAME_CHECK_FAILED.format(self.minecraft_nickname.value))
            return

        embed = NethexFormEmbed(interaction, self)
        await self.sendFormEphemeral(embed, interaction)
        await self.sendFormInChannel(embed, interaction)
        await self.sendFormToUser(embed, interaction)

    @staticmethod
    async def sendFormToUser(embed, interaction):
        await interaction.user.send(content=NethexLang.MODAL_MESSAGE_SEND_TO_USER, embed=embed)

    async def sendFormInChannel(self, embed, interaction):
        from reqconfbot.cogs.nethex import NethexCog
        await interaction.guild.get_channel(NethexCog.database.get(self.guild_id).forms_channel_id).send(embed=embed, view=NethexFormView())

    @staticmethod
    async def sendFormEphemeral(embed, interaction):
        await interaction.respond(NethexLang.MODAL_MESSAGE_SEND_EPHEMERAL, ephemeral=True, embed=embed)


class PanelCreatorLangView(View, ABC):

    def __init__(self):
        super().__init__(timeout=None)
        self.modal: Optional[Modal] = None

    @ui.button(label=PanelCreatorLang.VIEW_BUTTON_LABEL, style=ButtonStyle.green, custom_id="ViewSendModalRequest:view:button")
    async def send_modal(self, _, interaction: Interaction):
        modal = self.getFormModal(interaction)
        await interaction.response.send_modal(modal)

    @abstractmethod
    def getFormModal(self, interaction: Interaction) -> Modal:
        pass


class NethexPanelCreatorLangView(PanelCreatorLangView):
    def getFormModal(self, interaction: Interaction) -> Modal:
        return NethexFormModal(interaction.guild_id)
