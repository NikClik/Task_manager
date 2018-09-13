from sqlalchemy import create_engine, update, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pack.db.tables import Task
from pack.setting import *
from datetime import *

engine = create_engine(str(connect_str_to_db()))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class TaskFunctions:

    @classmethod
    def add_task(cls, task):
        session.add(task)
        session.commit()
        session.close()

    @classmethod
    def delete_task(cls, task_id):
        task = session.query(Task).filter(Task.id == task_id).first()
        session.delete(task)
        session.commit()
        session.close()

    @classmethod
    def get_all_task(cls):
        task = session.query(Task).all()
        session.close()
        return task

    @classmethod
    def get_task_by_id(cls, id):
        task = session.query(Task).filter(Task.id == id).first()
        session.close()
        return task

    @classmethod
    def change_date_time_task(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"date_of_start": (task.date_of_start,),
                                                               "time_of_start": (task.time_of_start,),
                                                               "date_of_end": (task.date_of_end,),
                                                               "time_of_end": (task.time_of_end,)})
        session.commit()
        session.close()

    @classmethod
    def change_task(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"header": (task.header,),
                                                               "priority": (task.priority,),
                                                               "tags": (task.tags,),
                                                               "comment": (task.comment,)})
        session.commit()
        session.close()

    @classmethod
    def change_expert(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"expert": (task.expert,)})
        session.commit()
        session.close()

    @classmethod
    def count_of_complite_task(cls, id):
        count = session.query(func.count(Task.id)).filter(Task.parent_task_id == id, Task.status == "Выполнено").\
            group_by(Task.id)
        session.close()
        return count

    @classmethod
    def change_task_status(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"status": (task.status,)})
        session.commit()
        session.close()

    @classmethod
    def actions_parent(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"is_parent_task": (task.is_parent_task,),
                                                               "under_task_id": (task.under_task_id,)})
        session.commit()
        session.close()

    @classmethod
    def actions_child(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"is_under_task": (task.is_under_task,),
                                                               "parent_task_id": (task.parent_task_id,),
                                                               "expert": (task.expert,)})
        session.commit()
        session.close()

    @classmethod
    def actions_linked(cls, task):
        session.query(Task).filter(Task.id == task.id).update({"is_linked": (task.is_linked,),
                                                               "linked_task_id": (task.linked_task_id,)})
        session.commit()
        session.close()

    @classmethod
    def group_by_tags(cls):
        tasks = session.query(Task).order_by(Task.tags.desc())
        session.close()
        return tasks

    @classmethod
    def group_by_status(cls):
        tasks = session.query(Task).order_by(Task.status.desc())
        session.close()
        return tasks

    @classmethod
    def search_by_header(cls, search_info):
        tasks = session.query(Task).filter(Task.header.like(str(search_info))).from_self()
        session.close()
        return tasks

    @classmethod
    def search_by_tag(cls, search_info):
        tasks = session.query(Task).filter(Task.tags.like(str(search_info))).from_self()
        session.close()
        return tasks

    @classmethod
    def get_user_tasks(cls, login):
        tasks = session.query(Task).filter(Task.owner == login).all()
        session.close()
        return tasks

    @classmethod
    def search_by_tags(cls, search_info):
        tasks = session.query(Task).filter(Task.tags.like(str(search_info))).from_self()
        session.close()
        return tasks

    @classmethod
    def search_by_priority(cls, search_info):
        tasks = session.query(Task).filter(Task.priority.like(str(search_info))).from_self()
        session.close()
        return tasks

    @classmethod
    def search_by_status(cls, search_info):
        tasks = session.query(Task).filter(Task.status.like(str(search_info))).from_self()
        session.close()
        return tasks

