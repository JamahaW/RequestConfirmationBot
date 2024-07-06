from __future__ import annotations
from __future__ import annotations
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

from reqconfbot.bots import BotType
from reqconfbot.constants.nethex import NethexForm
from reqconfbot.constants.panelcreator import PanelCreator
from reqconfbot.forms import ModalTextBuilder


class PanelCreatorEmbed(Embed):
    def __init__(self, createPanelModal: PanelCreatorModal):
        super().__init__(
            author=EmbedAuthor(createPanelModal.author.value),
            thumbnail=createPanelModal.thumbnail_url.value,
            description=createPanelModal.description.value,
            image=createPanelModal.banner_url.value,
            title=createPanelModal.theme.value,
            color=Color.gold()
        )


class PanelCreatorModal(ModalTextBuilder):

    def __init__(self, bot_type: BotType):
        super().__init__(title=PanelCreator.MODAL_TITLE)
        self.form_type: BotType = bot_type

        self.author = self.add(InputText(
            label=PanelCreator.MODAL_AUTHOR_LABEL,
            placeholder=PanelCreator.MODAL_AUTHOR_PLACEHOLDER,
            min_length=4,
            max_length=32,
            style=InputTextStyle.singleline
        ))

        self.thumbnail_url = self.add(InputText(
            label=PanelCreator.MODAL_THUMBNAIL_URL_LABEL,
            placeholder=PanelCreator.MODAL_THUMBNAIL_URL_PLACEHOLDER,
            style=InputTextStyle.short,
            required=False
        ))

        self.theme = self.add(InputText(
            label=PanelCreator.MODAL_THEME_LABEL,
            placeholder=PanelCreator.MODAL_THEME_PLACEHOLDER,
            min_length=8,
            max_length=40,
            style=InputTextStyle.singleline
        ))

        self.description = self.add(InputText(
            label=PanelCreator.MODAL_DESCRIPTION_LABEL,
            placeholder=PanelCreator.MODAL_DESCRIPTION_PLACEHOLDER,
            min_length=20,
            max_length=1000,
            style=InputTextStyle.long
        ))

        self.banner_url = self.add(InputText(
            label=PanelCreator.MODAL_BANNER_URL_LABEL,
            placeholder=PanelCreator.MODAL_BANNER_URL_PLACEHOLDER,
            style=InputTextStyle.short,
            required=False
        ))

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(
            embed=PanelCreatorEmbed(self),
            view=PanelCreatorView.make(self.form_type)
        )


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
            title=NethexForm.EMBED_TITLE.format(user.name),
            color=Color.gold(),
            author=EmbedAuthor(name=user.display_name, icon_url=user.display_avatar.url),
            footer=self.dumpInFooter(user, modal.minecraft_nickname.value),
            thumbnail=user.display_avatar.url
        )

        self.add_field(name=NethexForm.EMBED_FIELD_NAME, value=modal.minecraft_nickname.value, inline=True)
        self.add_field(name=NethexForm.EMBED_FIELD_SERVERS_PLAYED_ON, value=modal.played_servers.value, inline=False)
        self.add_field(name=NethexForm.EMBED_FIELD_SEASON_PLANNINGS, value=modal.user_plannings.value, inline=False)

        if modal.etc.value:
            self.add_field(name=NethexForm.EMBED_FIELD_INFO, value=modal.etc.value, inline=False)


class NethexFormButton(Button["ViewUserForm"], ABC):

    def __init__(self, label: str, style: ButtonStyle, color: Color, status: str):
        super().__init__(label=label, custom_id=f"ButtonUserForm:{label}", style=style)
        self.status = status
        self.color = color

    @abstractmethod
    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        """Поведение кнопки формы"""

    async def callback(self, interaction: Interaction):
        self.view.disable_all_items()
        embed = interaction.message.embeds[0]
        await self.updateEmbedStatus(embed)

        member, nickname = await self.getMemberAndNickname(embed, interaction)
        await self.memberProcess(interaction, member, embed, nickname)
        await interaction.edit(view=self.view, embed=embed)

    async def updateEmbedStatus(self, embed):
        embed.title = f"{self.status} ({embed.author.name})"

    @staticmethod
    async def getMemberAndNickname(embed, interaction):
        member_id, nickname = NethexFormEmbed.parseFromFooter(embed.footer)
        return (
            interaction.guild.get_member(member_id),
            nickname
        )


class NethexFormApplyButtonButton(NethexFormButton):
    def __init__(self):
        super().__init__(label=NethexForm.APPLY_BUTTON_LABEL, style=ButtonStyle.green, color=Color.green(), status=NethexForm.APPLY_BUTTON_STATUS)

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        embed.add_field(name="Сервер", value=interaction.guild.name, inline=True)
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
        super().__init__(title=NethexForm.DENY_MODAL_TITLE.format(nickname))

        self.reason = self.add(InputText(
            style=InputTextStyle.singleline,
            value=NethexForm.DENY_MODAL_VALUE,
            label=NethexForm.DENY_MODAL_LABEL,
            min_length=8,
            max_length=32
        ))

        self.member = member
        self.embed = embed

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.embed.add_field(name=NethexForm.DENY_EMBED_FIELD_DENY_REASON, value=self.reason.value, inline=False)
        await self.member.send(embed=self.embed)


class NethexFormDenyButtonButton(NethexFormButton):

    def __init__(self):
        super().__init__(label=NethexForm.DENY_BUTTON_TITLE, style=ButtonStyle.red, color=Color.red(), status=NethexForm.DENY_BUTTON_STATUS)

    async def memberProcess(self, interaction: Interaction, member: Member, embed: Embed, nickname: str):
        await interaction.response.send_modal(NethexFormDenyModal(member, embed, nickname))


class NethexFormModal(ModalTextBuilder):
    MINECRAFT_NICKNAME_REGEX: ClassVar[str] = r'^[a-zA-Z0-9_]+$'

    def __init__(self, guild_id: int):
        super().__init__(title=NethexForm.MODAL_TITLE)
        self.guild_id = guild_id

        self.minecraft_nickname = self.add(InputText(
            style=InputTextStyle.singleline,
            label=NethexForm.MODAL_MINECRAFT_NICKNAME_LABEL,
            placeholder=NethexForm.MODAL_MINECRAFT_NICKNAME_PLACEHOLDER,
            min_length=3,
            max_length=16
        ))

        self.played_servers = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexForm.MODAL_PLAYED_SERVERS_LABEL,
            placeholder=NethexForm.MODAL_PLAYER_SERVERS_PLACEHOLDER,
            min_length=10,
            max_length=200
        ))

        self.user_plannings = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexForm.MODAL_PLANNINGS_LABEL,
            placeholder=NethexForm.MODAL_PLANNINGS_PLACEHOLDER,
            min_length=50,
            max_length=500
        ))

        self.etc = self.add(InputText(
            style=InputTextStyle.multiline,
            label=NethexForm.MODAL_INFO_LABEL,
            max_length=300,
            required=False
        ))

    @classmethod
    def checkNickname(cls, nickname: str) -> bool:
        return re.match(cls.MINECRAFT_NICKNAME_REGEX, nickname) is not None

    async def callback(self, interaction: Interaction):
        if not self.checkNickname(self.minecraft_nickname.value):
            await interaction.respond(NethexForm.MODAL_MINECRAFT_NICKNAME_CHECK_FAILED.format(self.minecraft_nickname.value))
            return

        embed = NethexFormEmbed(interaction, self)
        await self.sendFormEphemeral(embed, interaction)
        await self.sendFormInChannel(embed, interaction)
        await self.sendFormToUser(embed, interaction)

    @staticmethod
    async def sendFormToUser(embed, interaction):
        await interaction.user.send(content=NethexForm.MODAL_MESSAGE_SEND_TO_USER, embed=embed)

    async def sendFormInChannel(self, embed, interaction):
        from reqconfbot.cogs.nethex import NethexCog
        await interaction.guild.get_channel(NethexCog.database.get(self.guild_id).forms_channel_id).send(embed=embed, view=NethexFormView())

    @staticmethod
    async def sendFormEphemeral(embed, interaction):
        await interaction.respond(NethexForm.MODAL_MESSAGE_SEND_EPHEMERAL, ephemeral=True, embed=embed)


class PanelCreatorView(View, ABC):

    @staticmethod
    def make(bot_type: BotType) -> PanelCreatorView:
        match bot_type:
            case BotType.NETHEX:
                return NethexPanelCreatorView()

    def __init__(self):
        super().__init__(timeout=None)
        self.modal: Optional[Modal] = None

    @ui.button(label=PanelCreator.VIEW_BUTTON_LABEL, style=ButtonStyle.green, custom_id="ViewSendModalRequest:view:button")
    async def send_modal(self, _, interaction: Interaction):
        modal = self.getFormModal(interaction)
        await interaction.response.send_modal(modal)

    @abstractmethod
    def getFormModal(self, interaction: Interaction) -> Modal:
        pass


class NethexPanelCreatorView(PanelCreatorView):
    def getFormModal(self, interaction: Interaction) -> Modal:
        return NethexFormModal(interaction.guild_id)
