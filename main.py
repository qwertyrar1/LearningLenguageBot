import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from translation_phrase import translate
from phrase_generation import FINAL_PHRASE

#logging.basicConfig(
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#)

#logger = logging.getLogger(__name__)

TOKEN = '5217794948:AAGLdL5jnGWE_bT4ZyqCfCW_nuGr8SLz7Vg'


def start(update, context):
    update.message.reply_text('выбери язык')
    return 1


def translate_phrase(update, context):
    context.user_data['lenguage'] = update.message.text
    update.message.reply_text(
        f"переведи фразу:\n{FINAL_PHRASE}")
    return 2


def enter_phrase(update, context):
    context.user_data['phrase'] = update.message.text
    if context.user_data['phrase'] == translate(FINAL_PHRASE, str(context.user_data['lenguage'])):
        update.message.reply_text("молодчинка!, правильно перевел\n"
                                  "хочешь продолжить?")
        context.user_data.clear()
        return 3
    else:
        update.message.reply_text("некрутышк(, неправильно перевел\n"
                                  "правильный перевод:\n"
                                  f"{str(translate(FINAL_PHRASE, str(context.user_data['lenguage'])))}\n"
                                  "хочешь продолжить?")
        context.user_data.clear()
        return 3


def choice(update, context):
    choice = update.message.text
    if choice == 'да':
        update.message.reply_text('выбери язык')
        return 1
    elif choice == 'нет':
        return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END



def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],

    states = {
                 1: [MessageHandler(Filters.text & ~Filters.command, translate_phrase)],
                 2: [MessageHandler(Filters.text & ~Filters.command, enter_phrase)],
                 3: [MessageHandler(Filters.text & ~Filters.command, choice)]
             },

    fallbacks = [CommandHandler('stop', stop)]

    )

    dp.add_handler(conv_handler)

    dp.add_handler(MessageHandler(Filters.text, start))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
