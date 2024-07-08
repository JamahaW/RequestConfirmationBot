from reqconfbot.bots.zapretniki import ZapretnikiBot
from reqconfbot.launch import launchBot
from reqconfbot.utils.tools import Environment

if __name__ == "__main__":
    PATH_TO_DOT_ENV = ".env"

    env = Environment(PATH_TO_DOT_ENV)

    # bot = NethexBot(env)
    bot = ZapretnikiBot(env)

    launchBot(bot, env)
