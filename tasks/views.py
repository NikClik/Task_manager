from django.shortcuts import render
from pack.methods.task_methods import *
from pack.functions.task_functions import *
from tasks.forms import *
from datetime import datetime, timedelta
from accounts.views import *
from pack.db.tables import User
from sqlalchemy.exc import *
from itertools import groupby


def split_date(date):
    old_date = date.split("-")
    new_date = old_date[2] + '-' + old_date[1] + '-' + old_date[0]
    return new_date


def add_task(request):
    errors = []
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            header = form.cleaned_data.get('header')
            priority = form.cleaned_data.get('priority')
            tags = form.cleaned_data.get('tags')
            comment = form.cleaned_data.get('comment')
            date_of_start = form.cleaned_data.get('date_of_start')
            time_of_start = form.cleaned_data.get('time_of_start')
            date_of_end = form.cleaned_data.get('date_of_end')
            time_of_end = form.cleaned_data.get('time_of_end')
            new_date_of_start = split_date(str(date_of_start))
            new_date_of_end = split_date(str(date_of_end))
            status = form.cleaned_data.get('status')
            user = user_name_and_password()
            if date_of_end < date_of_start:
                errors.append('Дата окончания не должна раньше позже даты начала')
            else:
                new_task = Task(owner=user[0], header=header, priority=priority, tags=tags, comment=comment,
                                date_of_start=new_date_of_start, time_of_start=time_of_start,
                                date_of_end=new_date_of_end, time_of_end=time_of_end, status=status,
                                date_of_create=None, time_of_create=None, expert=None, id=None,
                                is_linked=None, is_under_task=None, is_parent_task=None, linked_task_id=None,
                                parent_task_id=None, under_task_id=None)
                TaskFunctions.add_task(new_task)
                return redirect("main_page")
    else:
        form = TaskForm()
    return render(request, 'tasks_html/add_task.html', {'form': form,
                                                        'errors': errors})


def parse_date(date):
    old_date = date.split("-")
    new_date = old_date[2] + '-' + old_date[1] + '-' + old_date[0]
    return new_date


def change_task(request, pk):
    user_login = user_name_and_password()
    errors = []
    task = TaskFunctions.get_task_by_id(pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            header = form.cleaned_data.get('header')
            priority = form.cleaned_data.get('priority')
            tags = form.cleaned_data.get('tags')
            comment = form.cleaned_data.get('comment')
            date_of_start = form.cleaned_data.get('date_of_start')
            time_of_start = form.cleaned_data.get('time_of_start')
            date_of_end = form.cleaned_data.get('date_of_end')
            time_of_end = form.cleaned_data.get('time_of_end')
            new_date_of_start = split_date(str(date_of_start))
            new_date_of_end = split_date(str(date_of_start))
            status = form.cleaned_data.get('status')
            if date_of_end < date_of_start:
                errors.append('Дата окончания не должна раньше позже даты начала')
            else:
                new_task = Task(id=pk, header=header, priority=priority, tags=tags, comment=comment,
                                date_of_start=new_date_of_start, time_of_start=time_of_start,
                                date_of_end=new_date_of_end, time_of_end=time_of_end, status=status,
                                date_of_create=None, time_of_create=None, expert=None,
                                is_linked=None, is_under_task=None, is_parent_task=None, linked_task_id=None,
                                parent_task_id=None, under_task_id=None, owner=None)
                TaskFunctions.change_task(new_task)
                TaskFunctions.change_date_time_task(new_task)
                TaskChangeMethods.change_status(user_login[0],user_login[1], pk, status)
                return redirect('main_page')
    else:
        form = TaskForm(initial={'header': task.header, 'priority': task.priority, 'tags': task.tags,
                                 'comment': task.comment, 'date_of_start': parse_date(task.date_of_start),
                                 'time_of_start': task.time_of_start, 'date_of_end': parse_date(task.date_of_end),
                                 'time_of_end': task.time_of_end})
    return render(request, 'tasks_html/change_task.html', {'form': form,
                                                           'task_pk': pk})


def main_page(request):
    user_login = user_name_and_password()
    tasks = TaskFunctions.get_user_tasks(user_login[0])
    count_of_task = len(tasks)
    count_of_complete_task = 0
    count_of_not_complete_task = 0
    count_of_in_progress_task = 0
    tasks_today = []
    tasks_week = []
    tasks_mounth = []
    for task in tasks:
        if task.status == 'Выполнено':
            count_of_complete_task += 1
        if task.status == 'В ожиданни выполнения':
            count_of_in_progress_task += 1
        if task.status == 'Не выполнено':
            count_of_not_complete_task += 1
        if datetime.strptime(task.date_of_start, '%d-%m-%Y') < datetime.now() < datetime.strptime(task.date_of_end, '%d-%m-%Y'):
            tasks_today.append(task.header)
        if datetime.strptime(task.date_of_start, '%d-%m-%Y') < datetime.now() + timedelta(days=7) < datetime.strptime(task.date_of_end, '%d-%m-%Y'):
            tasks_week.append(task.header)
        if datetime.strptime(task.date_of_start, '%d-%m-%Y') < datetime.now() + timedelta(days=30) < datetime.strptime(task.date_of_end, '%d-%m-%Y'):
            tasks_mounth.append(task.header)

    return render(request, 'main_page.html', {'count_of_task': count_of_task,
                                              'count_of_complete_task': count_of_complete_task,
                                              'count_of_not_complete_task': count_of_not_complete_task,
                                              'count_of_in_progress_task': count_of_in_progress_task,
                                              'tasks_today': tasks_today,
                                              'tasks_week': tasks_week,
                                              'tasks_mounth': tasks_mounth,
                                              'user_login': user_login[0]})


def plan_on_day(request):
    user_login = user_name_and_password()
    tasks = TaskFunctions.get_user_tasks(user_login[0])
    dict_list = list(tasks)
    duplicate_task_list = dict_list.copy()
    for task in dict_list:
        if (datetime.strptime(task.date_of_start, '%d-%m-%Y') <= datetime.now()
                    <= datetime.strptime(task.date_of_end, '%d-%m-%Y')) is False:
            duplicate_task_list.remove(task)
    return render(request, 'plan_on_day.html', {'tasks': duplicate_task_list})


def look_at_task(request, pk):
    task = TaskFunctions.get_task_by_id(pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TaskForm(initial={'id': pk, 'header': task.header, 'priority': task.priority, 'tags': task.tags,
                                 'comment': task.comment, 'date_of_start': parse_date(task.date_of_start),
                                 'time_of_start': task.time_of_start, 'date_of_end': parse_date(task.date_of_end),
                                 'time_of_end': task.time_of_end})
    return render(request, 'tasks_html/look_task.html', {'form': form})


def look_at_task_dt(request, pk):
    task = TaskFunctions.get_task_by_id(pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TaskForm(initial={'id': pk, 'header': task.header, 'priority': task.priority, 'tags': task.tags,
                                 'comment': task.comment, 'date_of_start': parse_date(task.date_of_start),
                                 'time_of_start': task.time_of_start, 'date_of_end': parse_date(task.date_of_end),
                                 'time_of_end': task.time_of_end})
    return render(request, 'tasks_html/look_task_dt.html', {'form': form})


def delete_task(request, pk):
    user_login = user_name_and_password()
    try:
        TaskDeleteMethods.delete_task(user_login[0], user_login[1], pk)
    except:
        pass
    return redirect('main_page')


def change_status_of_task(request, pk, status):
    user_login = user_name_and_password()
    TaskChangeMethods.change_status(user_login[0], user_login[1], pk, status)
    return redirect('plan_on_day')


def all_tasks(request):
    user_login = user_name_and_password()
    tasks = TaskFunctions.get_user_tasks(user_login[0])
    group_tags = list()
    for task in tasks:
        group_tags.append(task.tags)
    group_tags = [element for element, _ in groupby(group_tags)]
    if request.method == 'POST':
        form = SearchTasks(request.POST)
        if form.is_valid():
            search_info = form.cleaned_data.get('search_info')
            search_in = form.cleaned_data.get('search_in')
            date_of_start = form.cleaned_data.get('date_of_start')
            date_of_end = form.cleaned_data.get('date_of_end')
            return redirect('all_search_tasks', info=search_info, search_column=search_in,
                            date_of_start=str(date_of_start), date_of_end=str(date_of_end))
    else:
        form = SearchTasks()
    return render(request, 'tasks_html/all_tasks.html', {'tasks': tasks,
                                                         'form': form,
                                                         'group_tags': group_tags})


def all_search_tasks(request, info, search_column, date_of_start, date_of_end):
    user_login = user_name_and_password()
    tasks = list()
    new_date_of_start = datetime.strptime(date_of_start, '%Y-%m-%d')
    new_date_of_end = datetime.strptime(date_of_end, '%Y-%m-%d')
    if search_column == "Статус":
        tasks = TaskFunctions.search_by_status(info)
    elif search_column == "Приоритет":
        tasks = TaskFunctions.search_by_priority(info)
    elif search_column == "Название":
        tasks = TaskFunctions.search_by_header(info)
    duplicate_tasks = list(tasks).copy()
    for task in tasks:
        tasks_date_of_start = datetime.strptime(task.date_of_start, '%d-%m-%Y')
        if (task.owner != user_login[0]) is True:
            duplicate_tasks.remove(task)
        if (new_date_of_start <= tasks_date_of_start <= new_date_of_end) is True:
            pass
        else:
            try:
                duplicate_tasks.remove(task)
            except:
                pass
    return render(request, 'tasks_html/all_searched_tasks.html', {'tasks': duplicate_tasks})


def group_tasks(request, info):
    user_login = user_name_and_password()
    tasks = TaskFunctions.search_by_tag(info)
    duplicate_tasks = list(tasks).copy()
    for task in tasks:
        if task.owner != user_login[0]:
            duplicate_tasks.remove(task)
    return render(request, 'tasks_html/all_searched_tasks.html', {'tasks': duplicate_tasks})


def split_str(string):
    try:
        new_split = string.split(',')
        new_split = list(filter(None, new_split))
        return new_split
    except:
        return None


def delete_link_between_task(request, left_link_id, right_link_id):
    user_login = user_name_and_password()
    LinkedTaskMethods.delete_link_between_linked_task(user_login[0], user_login[1], left_link_id, right_link_id)
    return redirect('main_page')


def linked_action(request, pk):
    errors = []
    login = user_name_and_password()
    task = TaskFunctions.get_task_by_id(pk)
    linked_ids = split_str(task.linked_task_id)
    if request.method == "POST":
        form = LinkedTasksForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            error = LinkedTaskMethods.add_linked_task(login[0], login[1], pk, id)
            if error is None:
                return redirect('all_tasks')
            else:
                errors.append(error)
    else:
        form = LinkedTasksForm()
    return render(request, 'tasks_html/linked_actions.html', {'form': form,
                                                              'task_pk': pk,
                                                              'is_linked': task.is_linked,
                                                              'linked_id': linked_ids,
                                                              'errors': errors,
                                                              'left_id': pk})


def delete_parent_child_link(request, id, parent):
    user_login = user_name_and_password()
    ParentTaskMethods.delete_link_between_task(user_login[0], user_login[1], id, parent)
    return redirect('main_page')


def parent_actions(request, pk):
    errors = []
    child_task = TaskFunctions.get_task_by_id(pk)
    under_tasks = split_str(child_task.under_task_id)
    login = user_name_and_password()
    if request.method == "POST":
        form = ParentTaskForm(request.POST)
        if form.is_valid():
            parent_task_id = form.cleaned_data.get('parent_task_id')
            expert = form.cleaned_data.get('expert')
            error = ParentTaskMethods.add_parent_for_task(login[0], login[1], pk, parent_task_id, expert)
            if error is None:
                return redirect('all_tasks')
            else:
                errors.append(error)
    else:
        form = ParentTaskForm()
    return render(request, 'tasks_html/parent_actions.html', {'form': form,
                                                              'under_tasks': under_tasks,
                                                              'is_parent': child_task.is_parent_task,
                                                              'is_under_task': child_task.is_under_task,
                                                              'parent_id': child_task.parent_task_id,
                                                              'expert': child_task.expert,
                                                              'errors': errors,
                                                              'pk': pk})
