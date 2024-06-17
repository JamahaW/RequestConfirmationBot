from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.events import DiscordBotEventHandler
from reqconfbot.slashcommands import DiscordBotSlashCommandHandler


def main():
    logger.info("Request Confirmation bot")
    logger.debug(DiscordBotEventHandler())
    logger.debug(DiscordBotSlashCommandHandler())
    bot.run()
    logger.info("stopped")


if __name__ == '__main__':
    main()
