from reqconfbot.bots import BotType
from reqconfbot.launch import launchBot

if __name__ == "__main__":
    PATH_TO_DOT_ENV = ".env"
    BOT_TYPE = BotType.NETHEX

    launchBot(PATH_TO_DOT_ENV, BOT_TYPE)
