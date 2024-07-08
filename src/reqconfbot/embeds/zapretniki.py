from enum import Enum
from enum import auto
from typing import Optional

from discord import Attachment
from discord import Color
from discord import Embed
from discord import EmbedField
from discord import EmbedFooter
from discord import EmbedMedia
from discord import User


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
