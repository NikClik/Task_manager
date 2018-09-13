from django import forms
from pack.functions.user_functions import *
from tasks.views import *
from django.forms import HiddenInput

class TaskForm(forms.Form):
    PRIORITY_CHOICE = {
        (' ', ' '),
        ('Высокая', 'Высокая'),
        ('Средняя', 'Средняя'),
        ('Низкая', 'Низкая'),
    }
    STATUS_CHOICE = {
        (' ', ' '),
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
        ('В ожидании выполнения', 'В ожидании выполнения'),
    }
    header = forms.CharField(label='Название задачи')
    priority = forms.ChoiceField(choices=PRIORITY_CHOICE, label='Приоритет задачи')
    tags = forms.CharField(label='Группа')
    comment = forms.CharField(label='Комментарий')
    date_of_start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Дата начала')
    time_of_start = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Время начала')
    date_of_end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Дата окончания')
    time_of_end = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), label='Время окончания')
    status = forms.ChoiceField(choices=STATUS_CHOICE, label='Статус')


class LinkedTasksForm(forms.Form):
    id = forms.IntegerField()


class ParentTaskForm(forms.Form):
    parent_task_id = forms.IntegerField(label='Id родительской задачи')
    expert = forms.CharField(label='Выполняющий')


class SearchTasks(forms.Form):
    SEARCH_IN_CHOICE = {
        ('Статус', 'Статус'),
        ('Название', 'Название'),
        ('Приоритет', 'Приоритет'),
    }
    search_info = forms.CharField(label='Поиск инфо')
    date_of_start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'width': '30%'}), label='Дата начала')
    date_of_end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Дата окончания')
    search_in = forms.ChoiceField(choices=SEARCH_IN_CHOICE, label='Поиск по')