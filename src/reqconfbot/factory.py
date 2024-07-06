from reqconfbot.bots import BotType
from reqconfbot.bots.custombot import CustomBot
from reqconfbot.bots.nethex import NethexBot
from reqconfbot.forms.nethex import NethexPanelCreatorView
from reqconfbot.forms.nethex import PanelCreatorView
from reqconfbot.utils.tools import Environment


class Factory:
    @staticmethod
    def makeBot(bot_type: BotType, env: Environment) -> CustomBot:
        match bot_type:
            case BotType.NETHEX:
                return NethexBot(env.prefix, env.database_folder)

            case _:
                raise ValueError()

    @staticmethod
    def makePanelCreatorView(bot_type: BotType) -> PanelCreatorView:
        match bot_type:
            case BotType.NETHEX:
                return NethexPanelCreatorView()
