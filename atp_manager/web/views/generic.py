from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic as views

from atp_manager.auth_app.models import Profile
from atp_manager.common.helpers.helpers import get_names_of_people_involved_from_queryset, \
    get_names_of_first_four_people_suitable_for_task
from atp_manager.common.mixins.mixins import RedirectToDashboard
from atp_manager.web.models import Task


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'profile/login-page.html'


class DashboardManagerView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_closed_for_approval=True).filter(is_approved_finished=False)

        get_names_of_people_involved_from_queryset(tasks)
        return tasks


class DashboardMemberView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_closed_for_approval=False).filter(taken_by__user_id=self.request.user)


class DashboardView(LoginRequiredMixin, views.RedirectView):
    # permission_required = 'atp_admin'
    def get_redirect_url(self, *args, **kwargs):
        # user_role = Profile.objects.get(user=self.request.user).role
        if not self.request.user.is_staff:
            return reverse('dashboard member')
        else:
            return reverse('dashboard manager')


class HistoryView(views.ListView):
    model = Task
    template_name = 'web/history.html'
    context_object_name = 'tasks'

    # def get_queryset(self):
    #     return Task.objects.filter(is_approved_finished=True)

    def get_queryset(self):
        finished_tasks = Task.objects.filter(is_approved_finished=True)
        outstanding_tasks = Task.objects.filter(is_outstanding=True)
        return finished_tasks | outstanding_tasks


class RunningTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/running-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False) \
            .filter(is_closed_for_approval=False) \
            .filter(taken_by__user_id__isnull=False).distinct()
        get_names_of_people_involved_from_queryset(tasks)
        return tasks


class AvailableTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/available-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=False) \
            .filter(taken_by__user_id=None).filter(is_wanted_by=None)
        get_names_of_people_involved_from_queryset(tasks)
        return tasks

    def get_context_data(self, **kwargs):

        automation_members = list(Profile.objects.all().filter(professional_skill="Automation Engineering"))
        automation_members = get_names_of_first_four_people_suitable_for_task(automation_members)

        mechanical_members = list(Profile.objects.all().filter(professional_skill="Mechanical Engineering"))
        mechanical_members = get_names_of_first_four_people_suitable_for_task(mechanical_members)

        electrical_members = list(Profile.objects.all().filter(professional_skill="Electrical Engineering"))
        electrical_members = get_names_of_first_four_people_suitable_for_task(electrical_members)

        graphics_and_design_members = list(Profile.objects.all().filter(professional_skill="Graphics and Design"))
        graphics_and_design_members = get_names_of_first_four_people_suitable_for_task(graphics_and_design_members)

        operational_members = list(
            Profile.objects.all().filter(professional_skill="Operational Technologist")
        )
        operational_members = get_names_of_first_four_people_suitable_for_task(operational_members)

        kwargs['automation_members'] = automation_members
        kwargs['mechanical_members'] = mechanical_members
        kwargs['electrical_members'] = electrical_members
        kwargs['graphics_and_design_members'] = graphics_and_design_members
        kwargs['operational_members'] = operational_members
        return super().get_context_data(**kwargs)


class RequestedTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/requested-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False).filter(is_closed_for_approval=False) \
            .filter(taken_by__isnull=True).filter(is_wanted_by__isnull=False)
        for task in tasks:
            task.is_wanted_by_name = Profile.objects.all().get(pk=task.is_wanted_by)
        # get_names_of_people_involved_from_queryset(tasks)
        return tasks


class ClosedTasksView(LoginRequiredMixin, views.ListView):
    model = Task
    template_name = 'web/closed-tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(is_approved_finished=False) \
            .filter(is_closed_for_approval=True) \
            .filter(is_outstanding=False)
        get_names_of_people_involved_from_queryset(tasks)
        return tasks
