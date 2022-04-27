from django.contrib import admin

# Register your models here.

from atp_manager.web.models import Task


class TasksInlineAdmin(admin.StackedInline):
    model = Task


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'type')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


