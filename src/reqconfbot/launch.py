from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.events import DiscordBotEventHandler
from reqconfbot.slashcommands import DiscordBotSlashCommandHandler


def main():
    logger.info("Request Confirmation bot")

    event_handler = DiscordBotEventHandler()
    logger.debug(event_handler)

    slash_command_handler = DiscordBotSlashCommandHandler()
    logger.debug(slash_command_handler)

    bot.run()
    logger.info("stopped")


if __name__ == '__main__':
    main()
