import telebot

API_TOKEN = '6126485704:AAHlzWyChNw9ucl_7pkDBB_uuaPsxHf-LfQ'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    initial_message(message.chat.id)


from .commands import *
commands = {
    'hist_cmd': ('Гистограммы', hist_cmd)
}


# Список команд
def initial_message(chat_id):
    # Создаём клавиатуру
    markup = telebot.types.InlineKeyboardMarkup()

    # Возможные команды
    for cmd_name in commands:
        btn_text, cmd = commands[cmd_name]
        markup.add(
            telebot.types.InlineKeyboardButton(
                text=btn_text,
                callback_data=cmd_name
            )
        )

    # Отправляем сообщение с командами
    bot.send_message(chat_id, 'Выберите команду из списка',
                     reply_markup=markup)


def win_command_list(call: telebot.types.CallbackQuery):
    # Создаём клавиатуру
    markup = telebot.types.InlineKeyboardMarkup()

    # Возможные команды
    for cmd_name in commands:
        btn_text, cmd = commands[cmd_name]
        markup.add(
            telebot.types.InlineKeyboardButton(
                text=btn_text,
                callback_data=cmd_name
            )
        )

    # Отправляем сообщение с командами
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите команду из списка',
        reply_markup=markup)


# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: telebot.types.CallbackQuery):
    if call.data in commands:
        _, cmd_func = commands[call.data]
        cmd_func(call)
    elif call.data.startswith('hist_cmd'):
        hist_cmd_handler(call, call.data[8:])
    elif call.data.startswith('win'):
        win_command_list(call)


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
