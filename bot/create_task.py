from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from orm.alchemy import create_new_task, get_user_id

TASK_TEXT, TASK_DATE = range(2)


def create_task(update: Update, context: CallbackContext):
    user = update.message.from_user['first_name']

    update.message.reply_text(
        f'{user} ты можешь просто написать название задачи мне \n\n'
        'Команда "/cancel" для отмены добавление задачи'
    )
    return TASK_TEXT


def create_task_text(update: Update, context: CallbackContext):
    task_name = update.message.text
    context.bot_data['username'] = update.message.chat['username']
    context.bot_data['task_name'] = task_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Введите дату задачи в формате гггг-мм-дд:')
    return TASK_DATE


def create_task_date(update: Update, context: CallbackContext):
    task_date = update.message.text
    context.bot_data['task_date'] = task_date
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Задача создана, не подведи меня Нео')

    user_id = get_user_id(context.bot_data['username'])
    create_new_task(task_name=context.bot_data['task_name'],
                    task_date=context.bot_data['task_date'],
                    user_id=user_id)

    return ConversationHandler.END


