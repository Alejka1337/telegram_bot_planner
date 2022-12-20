from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from orm.alchemy import delete_task as del_task


GET_ID, DELETE_TASK = range(2)


def delete_task(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Введите номер задачи которую хотите удалить:')
    return GET_ID


def get_del_task(update: Update, context: CallbackContext):
    task_id = update.message.text
    context.bot_data['task_id'] = task_id
    reply_keyboard = [['Yes', 'No']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Вы уверены что хотите удалить задачу?', reply_markup=markup_key)
    return DELETE_TASK


def set_del_task(update: Update, context: CallbackContext):
    user_choose = update.message.text

    if user_choose == 'Yes':
        del_task(context.bot_data['task_id'])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Задача удалена')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Отмена удаления задачи')

    return ConversationHandler.END