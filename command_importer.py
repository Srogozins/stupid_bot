import json
import random
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler

def simple_response_wrapper(response):
    def callback(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=response)
    return callback

def random_response_wrapper(responses):
    def callback(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(responses))
    return callback

# TODO: allow to pass *args, **qwargs to callbacks for more flexibility
def inline_query_wrapper(result_callbacks, cache_time=0):
    def inline_query(bot, update):
        results = [callback() for callback in result_callbacks]
        bot.answerInlineQuery(update.inline_query.id,
                              results=results,
                              cache_time=cache_time)
    return inline_query

def simple_inline_response_wrapper(command, response):
    def callback():
        return InlineQueryResultArticle(
            id=uuid4(),
            title=command,
            input_message_content=InputTextMessageContent(response))
    return callback

def random_inline_response_wrapper(command, responses):
    def callback():
        return InlineQueryResultArticle(
            id=uuid4(),
            title=command,
            input_message_content=InputTextMessageContent(
                random.choice(responses)))
    return callback

def load_from_file(file_path):
    with open(file_path) as d_file:
        return json.load(d_file)

def import_commands_from_file(file_path, dispatcher):
    return import_commands(load_from_file(file_path), dispatcher)

def import_commands(data, dispatcher):
    inline_result_callbacks = []
    for c_data in data['simple_response']:
        handler = CommandHandler(c_data['command'],
                                 simple_response_wrapper(c_data['response']))
        dispatcher.add_handler(handler)

        if "inline" in c_data and c_data['inline']:
            command = c_data['command']
            if c_data['inline_command']:
                command = c_data['inline_command']
                inline_result_callbacks.append(
                        simple_inline_response_wrapper(command, c_data['response']))

    for c_data in data['random_response']:
        handler = CommandHandler(c_data['command'],
                                 random_response_wrapper(c_data['responses']))
        dispatcher.add_handler(handler)

        if "inline" in c_data and c_data['inline']:
            command = c_data['command']
            if c_data['inline_command']:
                command = c_data['inline_command']
                inline_result_callbacks.append(
                        random_inline_response_wrapper(command, c_data['responses']))

    # TODO: receive and pass through cache time and possibly other config
    if inline_result_callbacks:
        dispatcher.add_handler(InlineQueryHandler(
            inline_query_wrapper(inline_result_callbacks)))

    return dispatcher
