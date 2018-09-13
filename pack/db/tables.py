from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import *
from pack.setting import *
from sqlalchemy.orm import mapper


# Base = declarative_base()
engine = create_engine(connect_str_to_db())
metadata = MetaData()


users_table = Table('users', metadata,
    Column('login', String, primary_key=True),
    Column('password', String),
    Column('question', String),
    Column('answer', String)
)


class User(object):
    def __init__(self, login, password, question, answer):
        self.login = login
        self.password = password
        self.question = question
        self.answer = answer

    def __repr__(self):
        return "Пользователь: %s; \n" \
               "Пароль: %s; \n" \
               "Вопрос: %s; \n" \
               "Ответ: %s; \n \n" % (self.login, self.password, self.question, self.answer)


tasks_table = Table('tasks', metadata,
    Column('id', Integer, primary_key=True),
    Column('owner', String, default='None'),
    Column('header', String),
    Column('priority', String),
    Column('tags', String),
    Column('comment', String),
    Column('date_of_create', String, default=datetime.datetime.now().date()),
    Column('time_of_create', String, default=datetime.datetime.now().time()),
    Column('date_of_start', String),
    Column('time_of_start', String),
    Column('date_of_end', String),
    Column('time_of_end', String),
    Column('status', String),
    Column('expert', String, default='None'),
    Column('is_linked', String, default='None'),
    Column('linked_task_id', String, default='None'),
    Column('is_under_task', String, default='None'),
    Column('parent_task_id', Integer, default=0),
    Column('is_parent_task', String, default='None'),
    Column('under_task_id', String, default='None'),
)


class Task(object):
    def __init__(self, id, owner, header, priority, tags, comment, date_of_create, time_of_create,
                 date_of_start, time_of_start, date_of_end, time_of_end, status, expert, is_linked,
                 linked_task_id, is_under_task, parent_task_id, is_parent_task, under_task_id):
        self.id = id
        self.owner = owner
        self.header = header
        self.priority = priority
        self.tags = tags
        self.comment = comment
        self.date_of_create = date_of_create
        self.time_of_create = time_of_create
        self.date_of_start = date_of_start
        self.time_of_start = time_of_start
        self.date_of_end = date_of_end
        self.time_of_end = time_of_end
        self.status = status
        self.expert = expert
        self.is_linked = is_linked
        self.linked_task_id = linked_task_id
        self.is_under_task = is_under_task
        self.parent_task_id = parent_task_id
        self.is_parent_task = is_parent_task
        self.under_task_id = under_task_id

    def __repr__(self):
        return "id: %s \n" \
               "    Название: %s \n"\
               "    Приоритет: %s \n"\
               "    Группа: %s \n"\
               "    Комментарий: %s \n"\
               "    Дата и время создания: %s %s \n"\
               "    Дата и время начала: %s %s \n"\
               "    Дата и время окончания: %s %s \n"\
               "    Выполняющий: %s \n"\
               "    Является ли задача связанной: %s \n"\
               "    Связана с: %s \n"\
               "    Является подзадачей: %s \n"\
               "    id Родительской задачи: %s \n"\
               "    Является ли родительской задачей: %s \n" \
               "    Подзадачи: %s \n" % \
               (self.id, self.header, self.priority, self.tags, self.comment, self.date_of_create,
                self.time_of_create, self.date_of_start, self.time_of_start, self.date_of_end, self.time_of_end,
                self.status, self.expert, self.is_linked, self.linked_task_id, self.parent_task_id, self.is_parent_task,
                self.under_task_id)


mapper(User, users_table)
mapper(Task, tasks_table)
metadata.create_all(engine)


def create_tables():
    metadata.create_all(engine)

