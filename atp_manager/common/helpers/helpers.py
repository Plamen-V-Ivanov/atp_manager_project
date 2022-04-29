from atp_manager.auth_app.models import Profile
from atp_manager.web.models import Task


def get_names_of_people_involved_from_queryset(tasks):
    for task in tasks:
        if task.taken_by:
            names_of_people = [x.full_name for x in (list(task.taken_by.all()))]
            if len(names_of_people) > 0:
                task.taken_by_names = ', '.join(names_of_people)
                task.save()
    return tasks


def get_names_of_first_four_people_suitable_for_task(list_of_people):
    list_of_people = [x.full_name for x in list_of_people]
    if len(list_of_people) > 4:
        list_of_people = list_of_people[:4]
    return ", ".join(sorted(list_of_people))


def get_finished_tasks_count_by_category(category):
    tasks = list(
        Task.objects.all()
            .filter(category=f"{category}")
            .filter(is_approved_finished=True)
            .filter(is_closed_for_approval=True)
    )
    return len(tasks)


def get_members_names_and_count_by_category(category):
    members = list(Profile.objects.all().filter(professional_skill=f"{category}"))
    members_count = len(members)
    members = [x.full_name for x in members]
    members = ", ".join(sorted(members))
    return members, members_count
