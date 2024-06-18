from discord import ApplicationContext
from discord import Member
from discord import Option

from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.modals import TestModal
from reqconfbot.views import ConfirmView
from reqconfbot.views import CounterView
from reqconfbot.views import TestViewButtons2
from reqconfbot.views import TestViewSelectMenu
from reqconfbot.views import TicTacToeView


class SlashCommandHandler:

    @staticmethod
    @bot.slash_command()
    async def button_my_view(context: ApplicationContext):
        await context.respond("This is a button!", view=TestViewButtons2())

    @staticmethod
    @bot.slash_command()
    async def select_menu_demo(context: ApplicationContext):
        await context.respond("view", view=TestViewSelectMenu())

    @staticmethod
    @bot.slash_command()
    async def test_form(context: ApplicationContext):
        await context.send_modal(TestModal(title="Заявка тест"))

    @staticmethod
    @bot.slash_command(name='test_slash_command')
    async def __test(
            context: ApplicationContext,
            number: Option(int, description='Число в диапазоне от 1 до 10', required=True, min_value=1, max_value=10),
            member: Option(Member, description='Любой участник сервера', required=True),
            choice: Option(str, description='Выберите пункт из списка', required=True, choices=['Банан', 'Яблоко', 'Апельсин']),
            text: Option(str, description='Текст из нескольких слов', required=False, default=''),
            boolean: Option(bool, description='True или False', required=False, default=False)
    ):
        await context.delete()

        for argument in (number, boolean, member, text, choice):
            logger.debug(f'{argument} ({type(argument).__name__})\n')

    @staticmethod
    @bot.slash_command()
    async def ask(context: ApplicationContext):
        view = ConfirmView()
        await context.respond("Продолжить?", view=view)
        await view.wait()

        if view.confirmed is None:
            ret = "Время истекло"

        elif view.confirmed:
            ret = "Подтверждено"

        else:
            ret = "Отменено"

        await context.send(ret)

    @staticmethod
    @bot.slash_command()
    async def counter(context: ApplicationContext):
        await context.respond(view=CounterView())

    @staticmethod
    @bot.slash_command()
    async def tic(context: ApplicationContext):
        await context.send("Tic Tac Toe: X goes first", view=TicTacToeView(), reference=context.message)
