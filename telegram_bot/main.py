import telebot
from .config import TOKEN

API_TOKEN = TOKEN
bot = telebot.TeleBot(API_TOKEN)
messages_to_delete = {}


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
    if call.message.chat.id in messages_to_delete:
        bot.delete_messages(
            chat_id=call.message.chat.id,
            message_ids=messages_to_delete[call.message.chat.id]
        )
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
