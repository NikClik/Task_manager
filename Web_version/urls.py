"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from accounts import views as acc_func
from tasks import views as task_func


urlpatterns = [
    url('registration', acc_func.registration, name='registration'),
    url('login', acc_func.log_in, name='login'),
    url('log_out', acc_func.log_out, name='log_out'),
    url('change_password', acc_func.change_password, name='change_password'),
    url('add_task', task_func.add_task, name='add_task'),
    url('main_page', task_func.main_page, name='main_page'),
    url('plan_on_day', task_func.plan_on_day, name='plan_on_day'),
    url('all_tasks', task_func.all_tasks, name='all_tasks'),
    path('all_search_tasks/<str:info>/<str:search_column>/<str:date_of_start>/<str:date_of_end>',
         task_func.all_search_tasks, name="all_search_tasks"),
    path('all_group_tasks/<str:info>', task_func.group_tasks, name="all_group_tasks"),
    path('look_at_task/<int:pk>', task_func.look_at_task, name="look_task"),
    path('look_at_task_td/<int:pk>', task_func.look_at_task_dt, name="look_task_td"),
    path('delete_link_between_tasks/<int:left_link_id>/<int:right_link_id>', task_func.delete_link_between_task, name="delete_link_between_tasks"),
    path('linked_task/<int:pk>', task_func.linked_action, name="linked_task"),
    path('change_status_of_task/<int:pk>/<str:status>', task_func.change_status_of_task, name="change_status_of_task"),
    path('delete_task/<int:pk>', task_func.delete_task, name="delete_task"),
    path('task/<int:pk>', task_func.change_task, name="Task"),
    path('delete_link_beetwen_child_and_parent/<int:id>/<int:parent>', task_func.delete_parent_child_link, name="delete_link_beetwen_child_and_parent"),
    path('parent_task/<int:pk>', task_func.parent_actions, name="parent_task"),
]
