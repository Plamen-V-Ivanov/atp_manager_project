from django.views import generic as views

from atp_manager.auth_app.models import Profile
from atp_manager.common.helpers.helpers import get_finished_tasks_count_by_category, \
    get_members_names_and_count_by_category
from atp_manager.web.models import Task


class TeamView(views.TemplateView):
    template_name = 'web/team-details.html'

    def get_context_data(self, **kwargs):

        automation_members, automation_members_count = \
            get_members_names_and_count_by_category("Automation Engineering")

        mechanical_members, mechanical_members_count = \
            get_members_names_and_count_by_category("Mechanical Engineering")

        electrical_members, electrical_members_count = \
            get_members_names_and_count_by_category("Electrical Engineering")

        graphics_and_design_members, graphics_and_design_members_count = \
            get_members_names_and_count_by_category("Graphics and Design")

        operational_technologist_members, operational_technologist_members_count = \
            get_members_names_and_count_by_category("Operational Technologist")

        automation_tasks = get_finished_tasks_count_by_category("Automation Engineering")

        mechanical_tasks = get_finished_tasks_count_by_category("Mechanical Engineering")

        electrical_tasks = get_finished_tasks_count_by_category("Electrical Engineering")

        graphics_and_design_tasks = get_finished_tasks_count_by_category("Graphics and Design")

        operational_tasks = get_finished_tasks_count_by_category("Operational Technologist")

        completed_tasks = list(
            Task.objects.all().filter(is_approved_finished=True).filter(is_closed_for_approval=True)
        )
        completed_tasks = len(completed_tasks)

        outstanding_tasks = list(
            Task.objects.all().filter(is_outstanding=True)
        )
        outstanding_tasks = len(outstanding_tasks)

        active_tasks = list(
            Task.objects.all().filter(is_approved_finished=False).filter(is_closed_for_approval=False)
        )
        active_tasks = len(active_tasks)

        kwargs['automation_members'] = automation_members
        kwargs['automation_members_count'] = automation_members_count
        kwargs['mechanical_members'] = mechanical_members
        kwargs['mechanical_members_count'] = mechanical_members_count
        kwargs['electrical_members'] = electrical_members
        kwargs['electrical_members_count'] = electrical_members_count
        kwargs['graphics_and_design_members'] = graphics_and_design_members
        kwargs['graphics_and_design_members_count'] = graphics_and_design_members_count
        kwargs['operational_technologist_members'] = operational_technologist_members
        kwargs['operational_technologist_members_count'] = operational_technologist_members_count

        kwargs['automation_tasks'] = automation_tasks
        kwargs['mechanical_tasks'] = mechanical_tasks
        kwargs['electrical_tasks'] = electrical_tasks
        kwargs['graphics_and_design_tasks'] = graphics_and_design_tasks
        kwargs['operational_tasks'] = operational_tasks
        kwargs['completed_tasks'] = completed_tasks
        kwargs['outstanding_tasks'] = outstanding_tasks
        kwargs['active_tasks'] = active_tasks

        return super().get_context_data(**kwargs)
