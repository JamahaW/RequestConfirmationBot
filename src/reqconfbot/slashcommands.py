from discord import ApplicationContext
from discord import Member
from discord import Option
from discord.ui import View

from reqconfbot.buttons import CounterButton
from reqconfbot.core import bot
from reqconfbot.core import logger
from reqconfbot.modals import TestModal
from reqconfbot.views import PersistentView
from reqconfbot.views import ViewConfirm
from reqconfbot.views import ViewSelectMenuTest
from reqconfbot.views import ViewTestButtons
from reqconfbot.views import ViewTicTacToe


class SlashCommandHandler:

    @staticmethod
    @bot.slash_command()
    async def test_slash_command_args(
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
    async def test_view_buttons(context: ApplicationContext):
        await context.respond("This is a button!", view=ViewTestButtons())

    @staticmethod
    @bot.slash_command()
    async def test_view_select(context: ApplicationContext):
        await context.respond("view", view=ViewSelectMenuTest())

    @staticmethod
    @bot.slash_command()
    async def test_view_persistent(ctx: ApplicationContext):
        await ctx.send("Любимый цвет?", view=PersistentView())

    @staticmethod
    @bot.slash_command()
    async def test_modal(context: ApplicationContext):
        await context.send_modal(TestModal(title="Заявка тест"))

    @staticmethod
    @bot.slash_command()
    async def test_button_counter(
            context: ApplicationContext,
            counter_text: Option(str, description="Текст счётчика", default=None)
    ):
        await context.respond(view=View(
            CounterButton(counter_text),
            timeout=None
        ))

    @staticmethod
    @bot.slash_command()
    async def test_etc_ask(context: ApplicationContext):
        view = ViewConfirm()
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
    async def test_etc_tic(context: ApplicationContext):
        await context.send("Tic Tac Toe: X goes first", view=ViewTicTacToe(), reference=context.message)
