from telebot import types


def yesno_keyboard(title, yes_text, no_text):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(yes_text, callback_data=title+';1'),
           types.InlineKeyboardButton(no_text, callback_data=title+';0'))

    return kb
