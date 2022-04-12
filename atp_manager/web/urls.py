from django.urls import path

from atp_manager.web.views import show_index, show_profile, show_profile_tasks, show_available_tasks, \
    show_running_tasks, suggest_a_task, show_team, add_a_note

urlpatterns = [
    path('', show_index, name='home page'),
    path('profile/<int:pk>/', show_profile, name='show profile'),
    path('profile/<int:pk>/tasks/', show_profile_tasks, name='profile active tasks'),
    path('profile/available_tasks/', show_available_tasks, name='show available tasks'),
    path('profile/running_tasks/', show_running_tasks, name='show running tasks'),
    path('profile/suggest_tasks/', suggest_a_task, name='suggest a task'),
    path('profile/add_note/', add_a_note, name='add note'),
    path('team/', show_team, name='show team'),


]
