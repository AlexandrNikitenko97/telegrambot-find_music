from Download import handle
from config import bot, help_message, start_message


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.from_user.id, "Hey {0} {1}!\n{2}".format(
                                                                 message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 start_message))


@bot.message_handler(commands=["help"])
def command_help(message):
    bot.send_message(message.from_user.id, help_message)


@bot.message_handler(content_types=["text"])
def send_audio(message):
    try:
        handle(message.from_user.id, message.text)
    except Exception:
        bot.send_message(message.from_user.id, "SORRY!\nSomething went wrong 😕\n(Size > 20 mg - Telegram limit)")


if __name__ == '__main__':
    bot.polling(none_stop=True)
