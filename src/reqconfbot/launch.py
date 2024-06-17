from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.slashcommands import SlashCommandHandler


def main():
    logger.info("Request Confirmation bot")
    logger.debug(SlashCommandHandler())
    bot.run()
    logger.info("stopped")


if __name__ == '__main__':
    main()
