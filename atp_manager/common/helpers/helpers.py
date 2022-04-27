def get_names_of_people_involved_from_queryset(tasks):
    for task in tasks:
        if task.taken_by:
            names_of_people = [x.full_name for x in (list(task.taken_by.all()))]
            if len(names_of_people) > 1:
                task.taken_by_names = ', '.join(names_of_people)
                task.save()
    return tasks
