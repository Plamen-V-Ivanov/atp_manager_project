from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic as views

from atp_manager.auth_app.models import Profile
from atp_manager.common.helpers.helpers import get_names_of_people_involved_from_queryset
from atp_manager.common.mixins.mixins import RedirectToDashboard
from atp_manager.web.models import Task


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'profile/login-page.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['hide_additional_nav_items'] = True
    #     return context


class DashboardManagerView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_closed_for_approval=True).filter(is_approved_finished=False)

        get_names_of_people_involved_from_queryset(tasks)
        return tasks

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     all_tasks = Task.objects.filter(is_closed_for_approval=True).filter(is_approved_finished=False)
    #     for task in all_tasks:
    #         if task.taken_by:
    #             task.taken_by_names = ', '.join(list(task.taken_by.all()))
    #     return context


class DashboardMemberView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_closed_for_approval=False).filter(taken_by__user_id=self.request.user)


# class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, views.RedirectView):
#     permission_required = 'is_staff'
#
#     def get_redirect_url(self, *args, **kwargs):
#         # user_role = Profile.objects.get(user=self.request.user).role
#         if not self.request.user.is_staff:
#             return reverse('dashboard member')
#         else:
#             return reverse('dashboard manager')

class DashboardView(LoginRequiredMixin, views.RedirectView):
    # permission_required = 'atp_admin'
    def get_redirect_url(self, *args, **kwargs):
        # user_role = Profile.objects.get(user=self.request.user).role
        if not self.request.user.is_staff:
            return reverse('dashboard member')
        else:
            return reverse('dashboard manager')

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_staff:
    #         def get_queryset(self):
    #             return Task.objects.filter(is_taken=True).filter(is_closed_for_approval=False).filter(
    #                 is_approved_finished=False)
    #
    #         return self.handle_no_permission()
    #
    #     def get_queryset(self):
    #         return Task.objects.filter(is_taken=True).filter(is_closed_for_approval=True).filter(
    #             is_approved_finished=False)
    #
    #     return super().dispatch(request, *args, **kwargs)


class HistoryView(views.ListView):
    model = Task
    template_name = 'web/history.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_approved_finished=True)


class RunningTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/running-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False) \
            .filter(is_closed_for_approval=False) \
            .filter(taken_by__user_id__isnull=False)
        get_names_of_people_involved_from_queryset(tasks)
        return tasks


class AvailableTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/available-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=False) \
            .filter(taken_by__user_id=None)
        get_names_of_people_involved_from_queryset(tasks)
        return tasks

    # def get_context_data(self, **kwargs):
    #     # tasks = super(AvailableTasksView, self).get_context_data()
    #     tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=False) \
    #         .filter(taken_by__user_id=None)
    #     for task in tasks:
    #         people = list(Profile.objects.filter(professional_skill=task.category))
    #         people_names = ', '.join([x.full_name for x in people])
    #         kwargs['people'] = {f'{task.category}': people_names}
    #     return super().get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        automation_members = list(Profile.objects.all().filter(professional_skill="Automation Engineering"))
        automation_members = [x.full_name for x in automation_members]
        automation_members = ",    ".join(sorted(automation_members))

        mechanical_members = list(Profile.objects.all().filter(professional_skill="Mechanical Engineering"))
        mechanical_members = [x.full_name for x in mechanical_members]
        mechanical_members = ",    ".join(sorted(mechanical_members))

        electrical_members = list(Profile.objects.all().filter(professional_skill="Electrical Engineering"))
        electrical_members = [x.full_name for x in electrical_members]
        electrical_members = ",    ".join(sorted(electrical_members))

        graphics_and_design_members = list(Profile.objects.all().filter(professional_skill="Graphics and Design"))
        graphics_and_design_members = [x.full_name for x in graphics_and_design_members]
        graphics_and_design_members = ",    ".join(sorted(graphics_and_design_members))

        operational_technologist_members = list(
            Profile.objects.all().filter(professional_skill="Operational Technologist"))
        operational_technologist_members = [x.full_name for x in operational_technologist_members]
        operational_technologist_members = ",    ".join(sorted(operational_technologist_members))

        kwargs['automation_members'] = automation_members
        kwargs['mechanical_members'] = mechanical_members
        kwargs['electrical_members'] = electrical_members
        kwargs['graphics_and_design_members'] = graphics_and_design_members
        kwargs['operational_technologist_members'] = operational_technologist_members
        return super().get_context_data(**kwargs)


class RequestedTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/requested-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=False) \
            .filter(taken_by_names="None")
        # get_names_of_people_involved_from_queryset(tasks)
        return tasks


class ClosedTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/closed-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=True)
        get_names_of_people_involved_from_queryset(tasks)
        return tasks
