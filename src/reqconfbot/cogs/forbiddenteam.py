from enum import Enum
from enum import auto
from typing import ClassVar
from typing import Optional

from discord import ApplicationContext
from discord import Bot
from discord import Color
from discord import Embed
from discord import EmbedField
from discord import EmbedFooter
from discord import Option
from discord import User
from discord.ext.commands import Cog
from discord.ext.commands import slash_command


class MinecraftDimensionType(Enum):
    OVERWORLD = auto()
    NETHER = auto()
    END = auto()

    def getName(self) -> str:
        return self.name.capitalize()


class MinecraftCoordinateEmbedField(EmbedField):

    @staticmethod
    def getCoordinateString(value: Optional[int], rounding: bool) -> str:
        if value is None:
            return "~"

        return f"{round(value, -1) if rounding else value}"

    def __init__(self, name: str, value: Optional[int], rounding: bool):
        super().__init__(name, self.getCoordinateString(value, rounding), True)


_coords_type = tuple[int, Optional[int], int]


class MinecraftCoordinatesEmbed(Embed):
    DIMENSIONS_COLORS: ClassVar[dict[MinecraftDimensionType, Color]] = {
        MinecraftDimensionType.OVERWORLD: Color.brand_green(),
        MinecraftDimensionType.NETHER: Color.red(),
        MinecraftDimensionType.END: Color.nitro_pink()
    }

    @classmethod
    def getDimensionColor(cls, dimension: MinecraftDimensionType) -> Color:
        return cls.DIMENSIONS_COLORS[dimension]

    @classmethod
    def buildFields(cls, coords: _coords_type, rounding: bool) -> list[EmbedField]:
        x, y, z = coords
        return [
            MinecraftCoordinateEmbedField("x", x, rounding),
            MinecraftCoordinateEmbedField("y", y, False),
            MinecraftCoordinateEmbedField("z", z, rounding),
        ]

    @classmethod
    def getTitle(cls, place_name: str, dimension: MinecraftDimensionType) -> str:
        return f"{place_name.capitalize()} ({dimension.name.capitalize()})"

    def __init__(
            self, *,
            dimension: MinecraftDimensionType,
            place_name: str,
            suggested_user: User,
            coords: _coords_type,
            rounding: bool
    ):
        super().__init__(
            color=self.getDimensionColor(dimension),
            title=self.getTitle(place_name, dimension),
            footer=EmbedFooter(suggested_user.name, suggested_user.avatar.url),
            fields=self.buildFields(coords, rounding)
        )


class ForbiddenCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="coords")
    async def showCoordinates(
            self,
            context: ApplicationContext,
            name: Option(str, "Название позиции"),
            dimension: Option(MinecraftDimensionType, "Измерение"),
            x: Option(int, "Позиция X"),
            z: Option(int, "Позиция Z"),
            y: Option(int, "Позиция Y", default=None),
            rounding: Option(bool, "Округление", default=True)
    ):
        await context.respond(embed=MinecraftCoordinatesEmbed(
            dimension=dimension,
            place_name=name,
            suggested_user=context.user,
            coords=(x, y, z),
            rounding=rounding
        ))
