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
from reqconfbot.utils.tools import ErrorsTyper


class SuggestedUserEmbedFooter(EmbedFooter):
    FOOTER_TEXT = "Предложил {0}"

    def __init__(self, user: User) -> None:
        super().__init__(self.FOOTER_TEXT.format(user.name), user.avatar)


class MinecraftDimensionType(Enum):
    OVERWORLD = auto()
    NETHER = auto()
    END = auto()

    def getName(self) -> str:
        return self.name.capitalize()


class MinecraftCoordinates:

    def __init__(self, x: int, y: Optional[int], z: int, rounding: bool) -> None:
        if rounding:
            x = round(x, -1)
            z = round(z, -1)

        if y is None:
            y = "~"

        self.string = f"```fix\n{x} {y} {z}\n```"


class MinecraftCoordinatesEmbed(Embed):
    DIMENSIONS_COLORS: ClassVar[dict[MinecraftDimensionType, Color]] = {
        MinecraftDimensionType.OVERWORLD: Color.brand_green(),
        MinecraftDimensionType.NETHER: Color.red(),
        MinecraftDimensionType.END: Color.nitro_pink()
    }

    @classmethod
    def getDimensionColor(cls, dimension: MinecraftDimensionType) -> Color:
        return cls.DIMENSIONS_COLORS[dimension]

    def __init__(
            self,
            dimension: MinecraftDimensionType,
            place_name: str,
            user: User,
            coords: MinecraftCoordinates,
            screenshot: Optional[Attachment]
    ):
        super().__init__(
            color=self.getDimensionColor(dimension),
            title=place_name.capitalize(),
            footer=SuggestedUserEmbedFooter(user)
        )
        self.add_field(name=dimension.name.capitalize(), value=coords.string)

        if screenshot is not None:
            self.image = EmbedMedia(screenshot.url)


class ForbiddenCog(Cog):

    def __init__(self, bot: Bot, databases_folder: Path):
        self.bot = bot
        self.database = ForbiddenTeamGuildDatabase(databases_folder)

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
        if (coords_channel_id := self.database.get(context.guild_id).coordinates_channel_id) is None:
            err = ErrorsTyper()
            err.add("Канал для вывода координат ещё не настроен")
            await err.respond(context)
            return

        coords_channel = context.guild.get_channel(coords_channel_id)
        await context.respond(f"Координаты отправлены в канал {coords_channel.jump_url}", ephemeral=True)
        await coords_channel.send(embed=(MinecraftCoordinatesEmbed(dimension, name, context.user, MinecraftCoordinates(x, y, z, rounding), screenshot)))

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
