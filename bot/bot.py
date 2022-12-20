from settings import TG_TOKEN
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters)

from create_task import create_task, create_task_text, create_task_date
from update_task import *
from delete_task import *
from show_tasks import show_all_task
from orm.alchemy import create_user


TOKEN = TG_TOKEN


COMMANDS = {'/help': 'Посмотреть список всех команд',
            '/tasks': 'Посмотреть список всех задач',
            '/create': 'Создать новую задачу',
            '/update': 'Обновить информацию о задаче (статус, регулярность, дату, приоритет)',
            '/delete': 'Удалить задачу',
            }

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

GET_CITY, GET_PHONE = range(2)
TASK_TEXT, TASK_DATE = range(2)
TASK_ID, TASK_OPTION, TASK_UPDATE = range(3)
GET_ID, DELETE_TASK = range(2)


def start(update: Update, context: CallbackContext):
    """Запуск бота через команду /start и запрос города пользователя"""
    username = update.message.chat['username']
    context.bot_data['username'] = username
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Рад приветствовать тебя {username} !")

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{username} давай познакомимся поближе! \n\n В каком городе ты живешь?")
    return GET_CITY


def get_city(update: Update, context: CallbackContext):
    """Получаем город который ввел пользователь и запрашиваем номер телефона"""
    city = update.message.text
    context.bot_data['city'] = city
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Хорошо так и запишем) \n\n'
                                  f'А теперь напиши свой номер что бы я мог с тобой связаться в случае чего')
    return GET_PHONE


def get_phone(update: Update, context: CallbackContext):
    """Получаем номер телефона и создаем пользователя в БД"""
    phone = update.message.text
    context.bot_data['phone'] = phone
    username = update.message.chat['username']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{username} благодарю за ответы \n\n '
                                  f'Посмотреть все функции бота можна с помощь команды /help')

    create_user(username=context.bot_data['username'],
                city=context.bot_data['city'],
                phone=context.bot_data['phone'])

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Очень жаль что ты передумал')
    return ConversationHandler.END


def help(update: Update, context: CallbackContext):
    """Вывод списка всех команд бота"""
    for command, command_text in COMMANDS.items():
        update.message.reply_text(f'{command} - {command_text}')
    return


def main():

    help_handler = CommandHandler('help', help)

    info_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_CITY: [MessageHandler(Filters.text, get_city)],
            GET_PHONE: [MessageHandler(Filters.text, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    create_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create_task)],
        states={
            TASK_TEXT: [MessageHandler(Filters.text, create_task_text)],
            TASK_DATE: [MessageHandler(Filters.text, create_task_date)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    update_handler = ConversationHandler(
        entry_points=[CommandHandler('update', update_task)],
        states={
            TASK_ID: [MessageHandler(Filters.text, get_task_id)],
            TASK_OPTION: [MessageHandler(Filters.text, get_option)],
            TASK_UPDATE: [MessageHandler(Filters.text, set_update)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    delete_handler = ConversationHandler(
        entry_points=[CommandHandler('delete', delete_task)],
        states={
            GET_ID: [MessageHandler(Filters.text, get_del_task)],
            DELETE_TASK: [MessageHandler(Filters.text, set_del_task)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    show_tasks_handler = CommandHandler('tasks', show_all_task)

    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(create_handler)
    dispatcher.add_handler(update_handler)
    dispatcher.add_handler(delete_handler)
    dispatcher.add_handler(show_tasks_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()