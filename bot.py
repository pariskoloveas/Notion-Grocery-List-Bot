import os
import logging
from telegram.ext import Updater, CommandHandler, Filters
from NotionService import NotionService
from typing import Type

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        self.setup()
        self.updater.start_polling()
        self.updater.idle()

    def setup(self) -> None:
        try:
            self.BOT_TOKEN: str = os.getenv('BOT_TOKEN')
            self.USERNAMES: str = os.getenv('TELEGRAM_USERNAMES').split(",")
            self.notion: NotionService = NotionService()
            self.updater: Type[Updater] = Updater(self.BOT_TOKEN, use_context=True)
            self.dispatcher = self.updater.dispatcher
            self.notion.setup_settings()
            self.register_handlers()
        except Exception as e:
            raise BotException(e)

    def register_handlers(self) -> None:
        self.dispatcher.add_handler(CommandHandler("start", self.start_command, Filters.user(username=self.USERNAMES)))
        self.dispatcher.add_handler(CommandHandler("list", self.list_command, Filters.user(username=self.USERNAMES)))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command, Filters.user(username=self.USERNAMES)))
        self.dispatcher.add_error_handler(self.error)

    def start_command(self, update, context) -> None:
        update.message.reply_text('Bot has started')

    def help_command(self, update, context) -> None:
        update.message.reply_text('Type /list to get the grocery list.')

    def list_command(self, update, context) -> None:
        data = '\n'.join(self.notion.get_grocery_list())
        logger.info('Successfully queried the database')
        update.message.reply_text(data)

    def error(self, update, context) -> None:
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)
        update.message.reply_text('an error occured')


class BotException(Exception):
    pass
