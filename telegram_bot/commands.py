import telebot
from data_processing.TableInterface import TableInterface
from data_processing.parsers import University
from .main import bot

interface = TableInterface()


def hist_cmd(call: telebot.types.CallbackQuery):
    # Получаем все вузы
    unis = interface.get_vuz_list()

    # Создаём клавиатуру для выбора вуза
    markup = telebot.types.InlineKeyboardMarkup()
    for uni in unis:
        markup.add(
            telebot.types.InlineKeyboardButton(
                text=uni.vuz_name,
                callback_data=f"hist_cmd{uni.short_name}"
            )
        )
    markup.add(
        telebot.types.InlineKeyboardButton(
            text='Назад',
            callback_data=f"win{'command_list'}"
        )
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите вуз, для которого нужно отобразить гистограмму',
        reply_markup=markup
    )


def hist_cmd_handler(call: telebot.types.CallbackQuery, vuz_name: str):
    vuz = interface.get_vuz_by_name(vuz_name)
    paths = interface.save_score_histogram_picture(vuz)
    media = []
    for path in paths:
        media.append(telebot.types.InputMediaPhoto(open(path, 'rb'), caption=vuz.vuz_name))

    bot.send_media_group(
        call.message.chat.id,
        media,
        
    )
