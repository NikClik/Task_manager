from sqlalchemy.exc import *
from pack.functions.task_functions import TaskFunctions
from pack.functions.user_functions import UsersFunctions
from pack.db.tables import Task
from datetime import datetime


class HelpMethods:

    @classmethod
    def check_on_valid_user(cls, login):
        users = UsersFunctions.get_user_by_login(login)
        if users is None:
            return False
        else:
            return True

    @classmethod
    def check_on_valid_task(cls, id):
        task = TaskFunctions.get_task_by_id(id)
        if task is None:
            return False
        else:
            return True

    @classmethod
    def check_datetime(cls, date_of_start, date_of_end, time_of_start, time_of_end):
        try:
            datetime.strptime(date_of_start, '%d-%m-%Y')
            datetime.strptime(date_of_end, '%d-%m-%Y')
            datetime.strptime(time_of_start, '%H:%M')
            datetime.strptime(time_of_end, '%H:%M')
            return True
        except:
            return False

    @classmethod
    def delete_sub_string_in_string(cls, string, sub_string):
        work_string = string.split(',')
        try:
            work_string.remove(str(sub_string))
            work_string = list(filter(None, work_string))
            new_string = ''
            for ids in work_string:
                new_string += ids + ','
            return new_string
        except:
            pass

    @classmethod
    def find_sub_sting_in_string(cls, string, substring):
        new_list = string.split(',')
        new_list = list(filter(None, new_list))
        try:
            new_list.index(str(substring))
            return True
        except:
            return False

    @classmethod
    def is_task_have_parent(cls, id):
        task = TaskFunctions.get_task_by_id(id)
        if task.parent_task_id == 0:
            return False
        else:
            return True

    @classmethod
    def task_is_under_task(cls, id):
        task = TaskFunctions.get_task_by_id(id)
        if task.is_under_task == 'Yes':
            return False
        else:
            return True

    @classmethod
    def check_under_task_and_parent_task_linked(cls, parent_id, child_id):
        child_task = TaskFunctions.get_task_by_id(child_id)
        if child_task.parent_task_id == int(parent_id):
            return True
        else:
            return False

    @classmethod
    def is_tasks_already_linked(cls, parent_id, child_id):
        parent_task = TaskFunctions.get_task_by_id(parent_id)
        child_task = TaskFunctions.get_task_by_id(child_id)
        left_link = HelpMethods.find_sub_sting_in_string(parent_task.linked_task_id, child_id)
        right_link = HelpMethods.find_sub_sting_in_string(child_task.linked_task_id, parent_id)
        if left_link is True and right_link is True:
            return True
        else:
            return False


class TaskAddMethods:

    @classmethod
    def add_task(cls, login, password, header, priority, tags, comment, date_of_start, time_of_start,
                 date_of_end, time_of_end, status):
        "Yes"
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        if datetime.strptime(date_of_end, '%d-%m-%Y') < datetime.strptime(date_of_start, '%d-%m-%Y'):
            print("Дата окончания не должна превышать дату начала")
        if user is None:
            print("Пароль или логин введен неверно")
        else:
            correct_date = HelpMethods.check_datetime(date_of_start, date_of_end, time_of_start, time_of_end)
            if correct_date:
                task = Task(owner=login, header=header, priority=priority, tags=tags, comment=comment,
                            date_of_start=date_of_start,
                            time_of_start=time_of_start, date_of_end=date_of_end, time_of_end=time_of_end,
                            status=status, id=None, date_of_create=None, time_of_create=None, expert=None,
                            is_linked=None, is_parent_task=None, is_under_task=None, linked_task_id=None,
                            parent_task_id=None, under_task_id=None)
                TaskFunctions.add_task(task)
                print("Задача добавлена")
            else:
                print("Одна из дат или время введены неверно, формат даты '11-11-2011', формат время '16:40'")


class TaskDeleteMethods:

    @classmethod
    def parse_and_delete_id_from_linked_task(cls, linked_task_id, deleted_id):
        try:
            old_task = TaskFunctions.get_task_by_id(linked_task_id)
            new_linked_id_string = HelpMethods.delete_sub_string_in_string(old_task.linked_task_id, deleted_id)
            if new_linked_id_string == '':
                task = Task(id=linked_task_id, is_linked='None', linked_task_id='None', comment=None,
                            date_of_create=None, priority=None, date_of_end=None, date_of_start=None,
                            time_of_create=None, time_of_end=None, expert=None, header=None, is_parent_task=None,
                            is_under_task=None, owner=None, parent_task_id=None, status=None, tags=None,
                            time_of_start=None, under_task_id=None)
                TaskFunctions.actions_linked(task)
            else:
                task = Task(id=linked_task_id, is_linked='Yes', linked_task_id=new_linked_id_string, comment=None,
                            date_of_create=None, priority=None, date_of_end=None, date_of_start=None,
                            time_of_create=None, time_of_end=None, expert=None, header=None, is_parent_task=None,
                            is_under_task=None, owner=None, parent_task_id=None, status=None, tags=None,
                            time_of_start=None, under_task_id=None
                            )
                TaskFunctions.actions_linked(task)
        except:
            pass

    @classmethod
    def delete_all_childs_of_task(cls, task_id):
        try:
            tasks = TaskFunctions.get_all_task()
            for delete_task in tasks:
                if delete_task.parent_task_id == int(task_id):
                    TaskFunctions.delete_task(delete_task.id)
        except:
            pass

    @classmethod
    def delete_form_childs_task_id(cls, task_id):
        try:
            tasks = TaskFunctions.get_all_task()
            for delete_task in tasks:
                is_task_child = HelpMethods.find_sub_sting_in_string(delete_task.under_task_id, task_id)
                if is_task_child:
                    new_under_task_id = HelpMethods.delete_sub_string_in_string(delete_task.under_task_id, task_id)
                    if new_under_task_id == '':
                        task = Task(id=delete_task.id, under_task_id='None', is_parent_task='None', expert='None',
                                    comment=None, date_of_create=None, priority=None, date_of_end=None,
                                    date_of_start=None, time_of_create=None, time_of_end=None, header=None,
                                    is_under_task=None, owner=None, parent_task_id=None, status=None, tags=None,
                                    time_of_start=None, is_linked=None, linked_task_id=None)
                        TaskFunctions.actions_child(task)
                    else:
                        task = Task(id=delete_task.id, under_task_id=new_under_task_id, is_parent_task='Yes',
                                    comment=None, date_of_create=None, priority=None, date_of_end=None,
                                    date_of_start=None, time_of_create=None, time_of_end=None, header=None,
                                    is_under_task=None, owner=None, parent_task_id=None, status=None, tags=None,
                                    time_of_start=None, is_linked=None, linked_task_id=None, expert=None)
                        TaskFunctions.actions_child(task)
        except:
            pass

    @classmethod
    def delete_task(cls, login, password, task_id):
        "Yes"
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        task = TaskFunctions.get_task_by_id(task_id)
        if user is None:
            print("Пароль или логин введен неверно")
        elif task is None:
            print("Данной задачи не существует")
        else:
            TaskFunctions.delete_task(task_id)
            TaskDeleteMethods.parse_and_delete_id_from_linked_task(task.linked_task_id, task_id)
            TaskDeleteMethods.delete_all_childs_of_task(task_id)
            TaskDeleteMethods.delete_form_childs_task_id(task_id)


class TaskChangeMethods:

    @classmethod
    def change_task_date(cls, login, password, id, date_of_start, date_of_end, time_of_start, time_of_end):
        "Yes"
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        task = TaskFunctions.get_task_by_id(id)
        if user is None:
            print("Пароль или логин введен неверно")
        elif task is None:
            print("Данной задачи не существует")
        elif task.owner != login:
            print("Вы не являетесь создателем данной задачи")
        else:
            correct_date = HelpMethods.check_datetime(date_of_start, date_of_end, time_of_start, time_of_end)
            if correct_date:
                task = Task(id=id, date_of_start=date_of_start, time_of_start=time_of_start,
                            date_of_end=date_of_end, time_of_end=time_of_end, comment=None, date_of_create=None,
                            priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                            parent_task_id=None, status=None, tags=None, is_linked=None, linked_task_id=None,
                            expert=None, is_parent_task=None, under_task_id=None)
                TaskFunctions.change_date_time_task(task)
            else:
                print("Неверно введены дата или время")

    @classmethod
    def change_expert(cls, login, password, id, expert):
        "Yes"
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        is_valid_task = TaskFunctions.get_task_by_id(id)
        is_valid_user = HelpMethods.check_on_valid_user(expert)
        if user is None:
            print("Пароль или логин введен неверно")
        elif is_valid_task is None:
            print("Данной задачи не существует")
        elif is_valid_task.owner != login:
            print("Вы не являетесь создателем данной задачи")
        else:
            is_task_under_task = HelpMethods.task_is_under_task(id)
            if is_task_under_task:
                task = Task(id=id, expert=expert, comment=None, date_of_create=None,
                            priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                            parent_task_id=None, status=None, tags=None, is_linked=None, linked_task_id=None,
                            is_parent_task=None, under_task_id=None, date_of_start=None, date_of_end=None,
                            time_of_end=None, time_of_start=None)
                TaskFunctions.change_expert(task)
            else:
                print("Данная задача не является подзадачей, вы не можете присвоит ей исполняющего")

    @classmethod
    def split_string(cls, string):
        tasks_id = string.split(',')
        tasks_id = list(filter(None, tasks_id))
        return tasks_id

    @classmethod
    def change_parent_task(cls, id):
        try:
            child_task = TaskFunctions.get_task_by_id(id)
            parent_task = TaskFunctions.get_task_by_id(child_task.parent_task_id)
            child_id_of_parent_task = TaskChangeMethods.split_string(parent_task.under_task_id)
            count_of_complete_task = TaskFunctions.count_of_complite_task(parent_task.id)
            if len(child_id_of_parent_task) == count_of_complete_task:
                new_tasks = Task(id=parent_task.id, status='Выполнено', comment=None, date_of_create=None,
                                 priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                                 parent_task_id=None, tags=None, is_linked=None, linked_task_id=None,
                                 expert=None, is_parent_task=None, under_task_id=None, time_of_start=None,
                                 date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.change_task_status(new_tasks)
            else:
                new_tasks = Task(id=parent_task.id, status='В процессе выполнения', comment=None, date_of_create=None,
                                 priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                                 parent_task_id=None, tags=None, is_linked=None, linked_task_id=None,
                                 expert=None, is_parent_task=None, under_task_id=None, time_of_start=None,
                                 date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.change_task_status(new_tasks)
        except:
            pass

    @classmethod
    def change_status_of_childs_tasks(cls, id):
        try:
            all_tasks = TaskFunctions.get_all_task()
            for task in all_tasks:
                if task.parent_task_id == id:
                    update_task = Task(id=task.id, status="Выполнено", comment=None, date_of_create=None,
                                       priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                                       parent_task_id=None, tags=None, is_linked=None, linked_task_id=None,
                                       expert=None, is_parent_task=None, under_task_id=None, time_of_start=None,
                                       date_of_end=None, date_of_start=None, time_of_end=None)
                    TaskFunctions.change_task_status(update_task)
        except:
            pass

    @classmethod
    def change_status(cls, login, password, id, status):
        "Yes"
        user = UsersFunctions.get_user_by_login_and_password(login, password)
        task = TaskFunctions.get_task_by_id(id)
        if user is None:
            print("Пароль или логин введен неверно")
        elif task is None:
            print("Данной задачи не существует")
        elif task.owner != login:
            print("Вы не являетесь создателем данной задачи")
        else:
            task = Task(id=id, status=status, comment=None, date_of_create=None,
                        priority=None, time_of_create=None, header=None, is_under_task=None, owner=None,
                        parent_task_id=None, tags=None, is_linked=None, linked_task_id=None,
                        expert=None, is_parent_task=None, under_task_id=None, time_of_start=None,
                        date_of_end=None, date_of_start=None, time_of_end=None)
            TaskFunctions.change_task_status(task)
            if status == 'Выполнено':
                TaskChangeMethods.change_status_of_childs_tasks(id)
                TaskChangeMethods.change_parent_task(id)

    @classmethod
    def change_task(cls, login, password, id, header, priority, tags, comment):
        "Yes"
        is_user_valid = UsersFunctions.get_user_by_login_and_password(login, password)
        is_task_valid = TaskFunctions.get_task_by_id(id)
        if is_user_valid is None:
            print("Пароль или логин введен неверно")
        elif is_task_valid is None:
            print("Данной задачи не существует")
        elif is_task_valid.owner != login:
            print("Вы не являетесь создателем данной задачи")
        else:
            task = Task(id=id, header=header, priority=priority, tags=tags, comment=comment, date_of_create=None,
                        time_of_create=None, is_under_task=None, owner=None, status=None,
                        parent_task_id=None, is_linked=None, linked_task_id=None,
                        expert=None, is_parent_task=None, under_task_id=None, time_of_start=None,
                        date_of_end=None, date_of_start=None, time_of_end=None)
            TaskFunctions.change_task(task)


class LinkedTaskMethods:

    @classmethod
    def add_linked_task(cls, login, password, id, linked_task_id):
        "Yes"
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        left_task = TaskFunctions.get_task_by_id(id)
        right_task = TaskFunctions.get_task_by_id(linked_task_id)
        is_task_already_linked = HelpMethods.is_tasks_already_linked(id, linked_task_id)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
            return "Пароль или логин введен неверно"
        elif left_task is None:
            print("Данной задачи не существует")
            return "Данной задачи не существует"
        elif right_task is False:
            print("Задачи, с которой вы пытаетесь связать, не существует")
            return "Задачи, с которой вы пытаетесь связать, не существует"
        elif right_task.owner != login or left_task.owner != login:
            print("Вы не являетесь владельцем данных задач")
            return "Вы не являетесь владельцем данных задач"
        elif id == linked_task_id:
            print("Вы не можете связать задачу с самой сабой")
            return "Вы не можете связать задачу с самой сабой"
        elif is_task_already_linked is True:
            print("Задачи уже связаны")
            return "Задачи уже связаны"
        else:
            if left_task.linked_task_id == 'None':
                new_task = Task(id=left_task.id, linked_task_id=str(right_task.id) + ',', is_linked='Yes', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            else:
                new_task = Task(id=left_task.id, linked_task_id=left_task.linked_task_id + str(right_task.id) + ',',
                                is_linked='Yes', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            if right_task.linked_task_id == 'None':
                new_task = Task(id=right_task.id, linked_task_id=str(left_task.id) + ',', is_linked='Yes', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            else:
                new_task = Task(id=right_task.id, linked_task_id=right_task.linked_task_id + str(left_task.id) + ',',
                                is_linked='Yes', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)

    @classmethod
    def delete_link_between_linked_task(cls, login, password, id, linked_task_id):
        "Yes"
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        left_task = TaskFunctions.get_task_by_id(id)
        right_task = TaskFunctions.get_task_by_id(linked_task_id)
        is_task_already_linked = HelpMethods.is_tasks_already_linked(id, linked_task_id)
        new_linked_str_for_left_task = HelpMethods.delete_sub_string_in_string(left_task.linked_task_id, linked_task_id)
        new_linked_str_for_right_task = HelpMethods.delete_sub_string_in_string(right_task.linked_task_id, id)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        elif left_task is None:
            print("Данной задачи не существует")
        elif right_task is False:
            print("Задачи, с которой вы пытаетесь связать, не существует")
        elif right_task.owner != login or left_task.owner != login:
            print("Вы не являетесь владельцем данных задач")
        elif id == linked_task_id:
            print("Вы не можете связать задачу с самой сабой")
        elif is_task_already_linked is not True:
            print("Задачи не связаны")
        else:
            if new_linked_str_for_left_task == '':
                new_task = Task(id=left_task.id, is_linked='None', linked_task_id='None', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            else:
                new_task = Task(id=left_task.id, is_linked='Yes', linked_task_id=new_linked_str_for_left_task,
                                comment=None, date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            if new_linked_str_for_right_task == '':
                new_task = Task(id=right_task.id, is_linked='None', linked_task_id='None', comment=None,
                                date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)
            else:
                new_task = Task(id=right_task.id, is_linked='Yes', linked_task_id=new_linked_str_for_right_task,
                                comment=None, date_of_create=None, time_of_create=None, expert=None,
                                priority=None, header=None, is_under_task=None, owner=None,
                                parent_task_id=None, tags=None, status=None,
                                is_parent_task=None, under_task_id=None, time_of_start=None,
                                date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_linked(new_task)


class ParentTaskMethods:

    @classmethod
    def add_parent_for_task(cls, login, password, id, parent_id, expert):
        "Yes"
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        is_child_has_parent_task = HelpMethods.is_task_have_parent(id)
        parent_task = TaskFunctions.get_task_by_id(parent_id)
        child_task = TaskFunctions.get_task_by_id(id)
        is_tasks_already_linked = HelpMethods.check_under_task_and_parent_task_linked(parent_id, id)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
            return "Пароль или логин введен неверно"
        if parent_task.owner != login or child_task.owner != login:
            print("Вы не являетесь создателем данных задач")
            return "Вы не являетесь создателем данных задач"
        if parent_task.is_parent_task == "Yes":
            print("Родительская задача уже является родителем")
            return "Родительская задача уже является родителем"
        if id == parent_id:
            print("Вы не можете пометить задаче как родительскую саму себя")
            return "Вы не можете пометить задаче как родительскую саму себя"
        if is_child_has_parent_task:
            print("У данной задачи уже есть родитель")
            return "У данной задачи уже есть родитель"
        if is_tasks_already_linked:
            print("Данные задачи уже связаны")
            return "Данные задачи уже связаны"
        if parent_task is None or child_task is None:
            print("Одной из задач не существует")
            return "Одной из задач не существует"
        else:
            if parent_task.under_task_id == 'None' and parent_task.is_parent_task == 'None':
                new_parent_task = Task(id=parent_id, under_task_id=str(id) + ',', is_parent_task='Yes', comment=None,
                                       date_of_create=None, time_of_create=None, expert=None,
                                       priority=None, header=None, is_under_task=None, owner=None,
                                       parent_task_id=None, tags=None, status=None,
                                       time_of_start=None, is_linked=None, linked_task_id=None,
                                       date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_parent(new_parent_task)
                new_child_task = Task(id=id, parent_task_id=parent_id, is_under_task='Yes', expert=expert, comment=None,
                                      date_of_create=None, time_of_create=None,
                                      priority=None, header=None, owner=None,
                                      tags=None, status=None, is_parent_task=None, under_task_id=None,
                                      time_of_start=None, is_linked=None, linked_task_id=None,
                                      date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_child(new_child_task)
            else:
                new_parent_task = Task(id=parent_id, under_task_id=parent_task.under_task_id + str(id) + ',',
                                       is_parent_task='Yes', expert=expert, comment=None,
                                       date_of_create=None, time_of_create=None,
                                       priority=None, header=None, owner=None,
                                       tags=None, status=None, is_under_task=None, parent_task_id=None,
                                       time_of_start=None, is_linked=None, linked_task_id=None,
                                       date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_parent(new_parent_task)
                new_child_task = Task(id=id, parent_task_id=int(id), is_under_task='Yes', expert=str(expert),
                                      comment=None, date_of_create=None, time_of_create=None,
                                      priority=None, header=None, owner=None,
                                      tags=None, status=None, is_parent_task=None, under_task_id=None,
                                      time_of_start=None, is_linked=None, linked_task_id=None,
                                      date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_child(new_child_task)

    @classmethod
    def delete_link_between_task(cls, login, password, id, parent_id):
        "Yes"
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        is_child_has_parent_task = HelpMethods.check_under_task_and_parent_task_linked(id, parent_id)
        parent_task = TaskFunctions.get_task_by_id(parent_id)
        child_task = TaskFunctions.get_task_by_id(id)
        new_str_of_id_for_parent_task = HelpMethods.delete_sub_string_in_string(parent_task.under_task_id, id)
        if parent_task is None or child_task is None:
            print("Одной из задач не существует")
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        if parent_task.owner != login or child_task.owner != login:
            print("Вы не являетесь создателем данных задач")
        if parent_task.is_parent_task == "Yes":
            print("Родительская задача уже является родителем")
        elif is_child_has_parent_task is False:
            print("У подзадачи нет родителя")
        else:
            new_child_task = Task(id=id, parent_task_id=0, is_under_task='None', expert='None', comment=None,
                                  date_of_create=None, time_of_create=None,
                                  priority=None, header=None, owner=None,
                                  tags=None, status=None, is_parent_task=None, under_task_id=None,
                                  time_of_start=None, is_linked=None, linked_task_id=None,
                                  date_of_end=None, date_of_start=None, time_of_end=None)
            TaskFunctions.actions_child(new_child_task)
            if new_str_of_id_for_parent_task == '':
                new_parent_task = Task(id=parent_id, is_parent_task='None', under_task_id='None', comment=None,
                                       date_of_create=None, time_of_create=None,
                                       priority=None, header=None, owner=None, parent_task_id=None,
                                       tags=None, status=None, expert=None, is_under_task=None,
                                       time_of_start=None, is_linked=None, linked_task_id=None,
                                       date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_parent(new_parent_task)
            else:
                new_parent_task = Task(id=parent_id, is_parent_task='Yes', under_task_id=new_str_of_id_for_parent_task,
                                       comment=None, date_of_create=None, time_of_create=None,
                                       priority=None, header=None, owner=None, parent_task_id=None,
                                       tags=None, status=None, expert=None, is_under_task=None,
                                       time_of_start=None, is_linked=None, linked_task_id=None,
                                       date_of_end=None, date_of_start=None, time_of_end=None)
                TaskFunctions.actions_parent(new_parent_task)


class ArchiveTask:

    @classmethod
    def is_task_archive(cls, task):
        date = TaskFunctions.get_task_by_id(id=task.id)
        current_date = datetime.now()
        if datetime.strptime(str(date.date_of_end), '%d-%m-%Y') < current_date:
            return True
        else:
            return False

    @classmethod
    def print_archive(cls, login, password):
        "Yes"
        tasks = TaskFunctions.get_all_task()
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is True and (task.owner == login or task.expert == login):
                    print(task)


    @classmethod
    def print_non_archived_tasks(cls, login, password):
        "Yes"
        tasks = TaskFunctions.get_all_task()
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)

    @classmethod
    def group_by_tags(cls, login, password):
        "Yes"
        tasks = TaskFunctions.group_by_tags()
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)

    @classmethod
    def group_by_status(cls, login, password):
        "Yes"
        tasks = TaskFunctions.group_by_status()
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)

    @classmethod
    def search_by_header(cls, login, password, search_info):
        "Yes"
        tasks = TaskFunctions.search_by_header(search_info)
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)

    @classmethod
    def search_by_tags(cls, login, password, search_info):
        "Yes"
        tasks = TaskFunctions.search_by_header(search_info)
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)

    @classmethod
    def search_by_status(cls, login, password, search_info):
        "Yes"
        tasks = TaskFunctions.search_by_header(search_info)
        is_valid_user = UsersFunctions.get_user_by_login_and_password(login, password)
        if is_valid_user is None:
            print("Пароль или логин введен неверно")
        else:
            for task in tasks:
                is_archive = ArchiveTask.is_task_archive(task)
                if is_archive is False and (task.owner == login or task.expert == login):
                    print(task)


# if __name__ == '__main__':
#     ArchiveTask.search_by_status('aa','aa', 'Задача 3')
#     ArchiveTask.print_non_archived_tasks('aa','aa')
#     ArchiveTask.group_by_tags('aa', 'aa')
#     TaskChangeMethods.change_parent_task(10)
#     i = 0
#     while i != 5:
#         TaskAddMethods.add_task('aaaa', 'aaaa', 'Здача 3', 'Низкий','Др','Комментарий 3','11-11-2018','16:40','22-11-2018', '16:40', 'Выполняется')
#         i += 1
#     HelpMethods.is_tasks_linked(1,2)
#     ParentTaskMethods.add_parent_for_task('aa', 'aa', 3, 2, 'aa')
#     LinkedTaskMethods.add_linked_task('aa', 'aa', 13, 14)
#     LinkedTaskMethods.delete_link_between_linked_task('aa', 'aa', 10, 11)
#     ParentTaskMethods.delete_link_between_task('aa','aa', 2, 1)
#     TaskDeleteMethods.delete_task('aa','aa',3)
#     LinkedTaskMethods.delete_link_between_linked_task('aa','aa',1,2)