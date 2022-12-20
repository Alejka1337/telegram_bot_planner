from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler
from orm.alchemy import select_all_task_for_user


def show_all_task(update: Update, context: CallbackContext):
    username = update.message.chat['username']
    all_tasks = select_all_task_for_user(username)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='<b>TASK_ID</b> | <b>TASK_NAME</b> | <b>STATUS</b> | <b>TASK_DATE</b> | <b>PRIORITY</b> | <b>REGULAR</b>',
                             parse_mode='HTML')

    for task in all_tasks:
        task_info_list = (str(task).split(" | "))
        print(task_info_list)

        if task_info_list[2] == 'False':
            task_info_list[2] = 'In plans'
        else:
            task_info_list[2] = 'Complete'

        if task_info_list[5] == 'False':
            task_info_list[5] = 'Not regular'
        else:
            task_info_list[5] = 'Regular'

        task_info_list[3] = task_info_list[3][:10]

        correct_task = ' | '.join(task_info_list)

        context.bot.send_message(chat_id=update.effective_chat.id, text=correct_task)
    return

