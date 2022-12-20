from sqlalchemy import create_engine, select, insert, delete
from sqlalchemy.orm import Session
from orm.models import Task, User
from settings import DATABASE_TYPE, USERNAME, PASSWORD, PORT, DATABASE_NAME

engine = create_engine(f"{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}", echo=True)


def create_user(username, city, phone):
    session = Session(engine)
    new_user = insert(User).values(username=username, city=city, phone=phone)
    session.execute(new_user)
    session.commit()
    session.close()
    return


def select_user(username):
    session = Session(engine)
    sel_user = session.scalar(select(User).where(User.username == username))
    session.commit()
    session.close()
    print(sel_user)
    return


def select_all_users():
    session = Session(engine)
    all_users = session.scalars(select(User))
    session.commit()
    session.close()
    for user in all_users:
        print(user)
    return


def create_new_task(task_name, task_date, user_id):
    session = Session(engine)
    new_task = insert(Task).values(task_name=task_name, task_date=task_date, username=user_id)
    session.execute(new_task)
    session.commit()
    session.close()
    return


def select_all_task():
    session = Session(engine)
    all_task = session.scalars(select(Task))
    for task in all_task:
        print(task)
    session.close()
    return


def select_all_task_for_user(username):
    session = Session(engine)
    select_user_id = session.scalar(select(User.id).where(User.username == username))
    all_tasks = session.scalars(select(Task).where(Task.username == select_user_id).order_by('task_date'))
    all_tasks_list = []
    for task in all_tasks:
        all_tasks_list.append(task)

    session.close()
    return all_tasks_list


def update_task_status(task_id):
    session = Session(engine)
    select_task = session.scalar(select(Task).where(Task.id == task_id))
    select_task.status = True
    session.commit()
    session.close()
    return


def update_task_priority(task_id, priority):
    session = Session(engine)
    select_task = session.scalar(select(Task).where(Task.id == task_id))
    select_task.priority = priority
    session.commit()
    session.close()
    return


def update_task_date(task_id, new_date):
    session = Session(engine)
    select_task = session.scalar(select(Task).where(Task.id == task_id))
    select_task.task_date = new_date
    session.commit()
    session.close()
    return


def update_task_regular(task_id):
    session = Session(engine)
    select_task = session.scalar(select(Task).where(Task.id == task_id))
    select_task.regular = True
    session.commit()
    return


def delete_task(task_id):
    session = Session(engine)
    session.execute(delete(Task).where(Task.id == task_id))
    session.commit()
    session.close()
    return


def get_user_id(username):
    session = Session(engine)
    user_id = session.scalar(select(User.id).where(User.username == username))
    session.commit()
    session.close()
    return user_id

