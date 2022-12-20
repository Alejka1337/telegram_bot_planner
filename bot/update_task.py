from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from orm.alchemy import update_task_date, update_task_status, update_task_regular, update_task_priority


TASK_ID, TASK_OPTION, TASK_UPDATE = range(3)


def update_task(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Введите номер задачи которую хотите обновить:')
    return TASK_ID


def get_task_id(update: Update, context: CallbackContext):
    task_id = update.message.text
    context.bot_data['task_id'] = task_id
    update.message.reply_text('''
        Команды для обновления:
        1) status – обновить статус задачи
        2) priority – обновить приоритет для задачи
        3) regular – сделать задачу регулярной
        4) date – обновить дату окончания задачи
    ''')
    return TASK_OPTION


def get_option(update: Update, context: CallbackContext):
    option = update.message.text
    context.bot_data['option'] = option

    if context.bot_data['option'] == 'status':
        reply_keyboard = [['Complete', 'In plans']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Обновить статус задачи', reply_markup=markup_key)
        return TASK_UPDATE

    elif context.bot_data['option'] == 'priority':
        update.message.reply_text('Установить приоритет задачи от 1 до 10')
        return TASK_UPDATE

    elif context.bot_data['option'] == 'regular':
        reply_keyboard = [['Regular', 'Not regular']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('Установить регулярность задачи', reply_markup=markup_key)
        return TASK_UPDATE

    elif context.bot_data['option'] == 'date':
        update.message.reply_text('Установить новую дату задачи (в формате гггг-мм-дд)')
        return TASK_UPDATE

    else:
        update.message.reply_text('Выбрана не верная опция')


def set_update(update: Update, context: CallbackContext):
    update_data = update.message.text
    context.bot_data['update_data'] = update_data
    print(context.bot_data)
    update.message.reply_text('Сохраняю изменения')

    if context.bot_data['option'] == 'status' and context.bot_data['update_data'] == 'Complete':
        update_task_status(context.bot_data['task_id'])

    elif context.bot_data['option'] == 'priority':
        update_task_priority(context.bot_data['task_id'], context.bot_data['update_data'])

    elif context.bot_data['option'] == 'date':
        update_task_date(context.bot_data['task_id'], context.bot_data['update_data'])

    elif context.bot_data['option'] == 'regular' and context.bot_data['update_data'] == 'Regular':
        update_task_regular(context.bot_data['task_id'])

    update.message.reply_text('Задача обновлена!')

    return ConversationHandler.END



