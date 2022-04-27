from django.urls import path

# from atp_manager.web.views import show_index, show_team, show_available_tasks, show_running_tasks, suggest_task, \
#     add_task, edit_task, delete_task

# urlpatterns = [
#
#     path('', show_index, name='index'),
#     path('team/', show_team, name='show team'),
#
#
#     path('tasks/available/', show_available_tasks, name='show available tasks'),
#     path('tasks/running/', show_running_tasks, name='show running tasks'),
#
#     path('task/suggest/', suggest_task, name='suggest a task'),
#     path('task/add/', add_task, name='add a task'),
#     path('task/edit<int:pk>/', edit_task, name='edit a task'),
#     path('task/delete/<int:pk>/', delete_task, name='delete a task'),
#
#
# ]
from atp_manager.web.views.generic import HomeView, AvailableTasksView, RunningTasksView, DashboardView, \
    DashboardManagerView, DashboardMemberView, HistoryView, RequestedTasksView, ClosedTasksView
from atp_manager.web.views.task import CreateTaskView, EditTaskView, DeleteTaskView, take_task, close_task, \
    approve_task_is_done, give_task, dont_approve_task_is_done, dont_give_task
from atp_manager.web.views.team import TeamView

urlpatterns = [

    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/manager/', DashboardManagerView.as_view(), name='dashboard manager'),
    path('dashboard/member/', DashboardMemberView.as_view(), name='dashboard member'),
    path('team/', TeamView.as_view(), name='show team'),
    path('history/', HistoryView.as_view(), name='show history'),

    path('tasks/available/', AvailableTasksView.as_view(), name='show available tasks'),
    path('tasks/running/', RunningTasksView.as_view(), name='show running tasks'),
    path('tasks/requested/', RequestedTasksView.as_view(), name='show requested tasks'),
    path('tasks/closed/', ClosedTasksView.as_view(), name='show closed tasks'),

    # path('task/suggest/', suggest_task, name='suggest a task'),
    path('task/add/', CreateTaskView.as_view(), name='add a task'),
    path('task/edit/<int:pk>/', EditTaskView.as_view(), name='edit a task'),
    path('task/delete/<int:pk>/', DeleteTaskView.as_view(), name='delete a task'),

    path('task/approve/<int:pk>/', approve_task_is_done, name='approve task is finished'),
    path('task/dont/approve/<int:pk>/', dont_approve_task_is_done, name='dont approve task is finished'),
    path('task/give/<int:pk>/', give_task, name='give task'),
    path('task/dont/give/<int:pk>/', dont_give_task, name='dont give task'),
    path('task/take/<int:pk>/', take_task, name='take task'),
    path('task/close/<int:pk>/', close_task, name='close task'),

]

