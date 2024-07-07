from enum import Enum
from enum import auto
from pathlib import Path
from typing import ClassVar
from typing import Optional

from discord import ApplicationContext
from discord import Attachment
from discord import Bot
from discord import Color
from discord import Embed
from discord import EmbedFooter
from discord import EmbedMedia
from discord import Option
from discord import TextChannel
from discord import User
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions
from discord.ext.commands import slash_command

from reqconfbot.databases.forbiddenteam import ForbiddenTeamGuildDatabase


class MinecraftDimensionType(Enum):
    OVERWORLD = auto()
    NETHER = auto()
    END = auto()

    def getName(self) -> str:
        return self.name.capitalize()


_coords_type = tuple[int, Optional[int], int]


class MinecraftCoordinatesEmbed(Embed):
    INTEND = 5

    DIMENSIONS_COLORS: ClassVar[dict[MinecraftDimensionType, Color]] = {
        MinecraftDimensionType.OVERWORLD: Color.brand_green(),
        MinecraftDimensionType.NETHER: Color.red(),
        MinecraftDimensionType.END: Color.nitro_pink()
    }

    @classmethod
    def getDimensionColor(cls, dimension: MinecraftDimensionType) -> Color:
        return cls.DIMENSIONS_COLORS[dimension]

    @classmethod
    def formatCoord(cls, value: str) -> str:
        return f"{value:<{cls.INTEND}}"

    @staticmethod
    def getCoordString(value: int, rounding: bool) -> str:
        if value is None:
            return "~"

        return f"{round(value, -1) if rounding else value}"

    @classmethod
    def getCoordinatesString(cls, coords: _coords_type, rounding: bool) -> str:
        x, y, z = coords
        x = cls.formatCoord(cls.getCoordString(x, rounding))
        y = cls.formatCoord(cls.getCoordString(y, False))
        z = cls.formatCoord(cls.getCoordString(z, rounding))
        return f"```fix\n{x} {y} {z}\n```"

    def __init__(
            self, *,
            dimension: MinecraftDimensionType,
            place_name: str,
            suggested_user: User,
            coords: _coords_type,
            rounding: bool,
            screenshot: Optional[Attachment]
    ):
        super().__init__(
            color=self.getDimensionColor(dimension),
            title=place_name.capitalize(),
            footer=EmbedFooter(suggested_user.name, suggested_user.avatar.url)
        )
        self.add_field(name=dimension.name.capitalize(), value=self.getCoordinatesString(coords, rounding))

        if screenshot is not None:
            self.image = EmbedMedia(screenshot.url)


class ForbiddenCog(Cog):

    def __init__(self, bot: Bot, databases_folder: Path):
        self.bot = bot
        self.database: ForbiddenTeamGuildDatabase = ForbiddenTeamGuildDatabase(databases_folder)

    @slash_command(name="coords")
    async def sendCoords(
            self,
            context: ApplicationContext,
            name: Option(str, "Название позиции"),
            dimension: Option(MinecraftDimensionType, "Измерение"),
            x: Option(int, "Позиция X"),
            z: Option(int, "Позиция Z"),
            y: Option(int, "Позиция Y", default=None),
            rounding: Option(bool, "Округление", default=True),
            screenshot: Option(Attachment, required=False)
    ):
        await context.respond(embed=MinecraftCoordinatesEmbed(
            dimension=dimension,
            place_name=name,
            suggested_user=context.user,
            coords=(x, y, z),
            rounding=rounding,
            screenshot=screenshot
        ))

    @slash_command(name="coords_set_channel")
    @has_permissions(administrator=True)
    async def setCoordsChannel(
            self,
            context: ApplicationContext,
            channel: TextChannel
    ):
        self.database.get(context.guild_id).coordinates_channel_id = channel.id
        self.database.dump()
        await context.respond(f"Теперь для координат используется канал {channel.jump_url}", ephemeral=True)
