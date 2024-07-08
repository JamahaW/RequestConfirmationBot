from __future__ import annotations

from enum import Enum
from enum import auto
from typing import ClassVar
from typing import Optional

from discord import Attachment
from discord import ButtonStyle
from discord import Color
from discord import Embed
from discord import EmbedAuthor
from discord import EmbedField
from discord import EmbedFooter
from discord import EmbedMedia
from discord import Guild
from discord import Interaction
from discord import Member
from discord import Role
from discord import User
from discord.ui import Button
from discord.ui import View
from discord.ui import button

from reqconfbot.utils.tools import ErrorsTyper
from reqconfbot.utils.tools import datetimeNow
from reqconfbot.utils.tools import getMemberByID


class Dimension(Enum):
    OVERWORLD = auto()
    NETHER = auto()
    END = auto()

    def getName(self) -> str:
        return self.name.capitalize()

    def getColor(self) -> Color:
        colors = {
            Dimension.OVERWORLD: Color.brand_green(),
            Dimension.NETHER: Color.red(),
            Dimension.END: Color.nitro_pink()
        }
        return colors[self]


class CoordinatesEmbedField(EmbedField):

    def __init__(self, dimension: Dimension, coords: tuple[int, ...], rounding: bool) -> None:
        x, y, z = coords

        if rounding:
            x = round(x, -1)
            z = round(z, -1)

        if y is None:
            y = "~"

        super().__init__(dimension.name.capitalize(), f"```fix\n{x} {y} {z}\n```", True)


class SuggestedUserEmbedFooter(EmbedFooter):
    FOOTER_TEXT = "Предложил {0}"

    def __init__(self, user: User) -> None:
        super().__init__(self.FOOTER_TEXT.format(user.name), user.avatar)


class CoordinatesEmbed(Embed):

    def __init__(self, user: User, place_name: str, dimension: Dimension, coordinates_embed_field: list[CoordinatesEmbedField], screenshot: Optional[Attachment]):
        super().__init__(
            color=dimension.getColor(),
            title=place_name.capitalize(),
            footer=SuggestedUserEmbedFooter(user),
            fields=coordinates_embed_field
        )

        if screenshot is not None:
            self.image = EmbedMedia(screenshot.url)


class TaskEmbedField(EmbedField):

    @staticmethod
    def fromID(user_id: int, guild: Guild) -> TaskEmbedField:
        return TaskEmbedField(getMemberByID(user_id, guild))

    def __init__(self, user: User | Member) -> None:
        super().__init__(datetimeNow(), user.mention, True)


class FooterPacker:
    VALUE_SEPARATOR: ClassVar[str] = ";"

    def __init__(self, footer: EmbedFooter) -> None:
        suggested, role, *actives = map(int, footer.text.split(self.VALUE_SEPARATOR))
        self.suggested_user_id: int = suggested
        self.speciality_id = role
        self.active_ids: list[int] = list(a.id for a in actives)

    @classmethod
    def cleanFooter(cls, suggested: User, speciality: Role) -> EmbedFooter:
        return EmbedFooter(f"{suggested.id}{cls.VALUE_SEPARATOR}{speciality.id}")

    def pack(self) -> EmbedFooter:
        return EmbedFooter(self.VALUE_SEPARATOR.join((str(i) for i in ([self.suggested_user_id] + self.active_ids))))


class TaskEmbed(Embed):

    def __init__(self, suggested_user: User, role: Role, text: str) -> None:
        super().__init__(
            color=role.color,
            author=EmbedAuthor(suggested_user.name, icon_url=suggested_user.avatar),
            description=f"### {role.mention}\n```fix\n{text.capitalize()}\n```",
            footer=FooterPacker.cleanFooter(suggested_user, role)
        )


class TaskView(View):
    MAX_USERS: ClassVar[int] = 25

    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def __parseMessage(interaction: Interaction) -> tuple[Embed, FooterPacker]:
        e = interaction.message.embeds[0]
        return e, (FooterPacker(e.footer))

    @button(label="Учавствовать", custom_id="TaskView::add_active_user", style=ButtonStyle.blurple)
    async def add_active_user(self, _: Button, interaction: Interaction):
        embed, footer_packer = self.__parseMessage(interaction)
        err = ErrorsTyper()

        if interaction.user.id in footer_packer.active_ids:
            err.add("Вы уже участвуете в этом задании!")

        need_role = interaction.guild.get_role(footer_packer.speciality_id)

        if need_role not in interaction.user.roles:
            err.add(f"Для выполнения этого задания нужна специальность {need_role.mention}")

        if len(embed.fields) == self.MAX_USERS:
            err.add("Из-за ограничений платформы может участвовать не более {0} человек".format(self.MAX_USERS))

        if err.isFailed():
            await err.respond(interaction)
            return

        footer_packer.active_ids.append(interaction.user.id)
        embed.fields.append(TaskEmbedField(interaction.user))
        embed.footer = footer_packer.pack()

        await interaction.edit(embed=embed)

    @button(label="Готово", custom_id="TaskView::send_task_status_done", style=ButtonStyle.green)
    async def send_task_status_done(self, _: Button, interaction: Interaction):
        embed, footer_packer = self.__parseMessage(interaction)
        err = ErrorsTyper()

        if footer_packer.suggested_user_id != interaction.user.id:
            err.add("Помечать как готовое может только создатель задания")

        if embed.footer is None:
            err.add("Задание уже выполнено!")

        if err.isFailed():
            await err.respond(interaction)
            return

        self.disable_all_items()
        embed.description = f"# Готово\n{datetimeNow()}\n{embed.description}"
        embed.remove_footer()

        await interaction.message.edit(embed=embed, view=self)
        await interaction.respond("Задание завершено!", ephemeral=True)
