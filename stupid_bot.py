import configparser
import logging
from telegram.ext import Updater

import command_importer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main(commands_file):
    config = configparser.ConfigParser()
    config.read('./botconfig.ini')
    updater = Updater(config['auth']['token'])
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error)
    # Import commands
    dispatcher = command_importer.import_commands_from_file(commands_file, dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main('commands.json')
