from django.views import generic as views

from atp_manager.auth_app.models import Profile


class TeamView(views.TemplateView):
    template_name = 'web/team-details.html'

    def get_context_data(self, **kwargs):
        automation_members = list(Profile.objects.all().filter(professional_skill="Automation Engineering"))
        automation_members = [x.full_name for x in automation_members]
        automation_members_count = len(automation_members)
        automation_members = ",    ".join(sorted(automation_members))

        mechanical_members = list(Profile.objects.all().filter(professional_skill="Mechanical Engineering"))
        mechanical_members = [x.full_name for x in mechanical_members]
        mechanical_members_count = len(mechanical_members)
        mechanical_members = ",    ".join(sorted(mechanical_members))

        electrical_members = list(Profile.objects.all().filter(professional_skill="Electrical Engineering"))
        electrical_members = [x.full_name for x in electrical_members]
        electrical_members_count = len(electrical_members)
        electrical_members = ",    ".join(sorted(electrical_members))

        graphics_and_design_members = list(Profile.objects.all().filter(professional_skill="Graphics and Design"))
        graphics_and_design_members = [x.full_name for x in graphics_and_design_members]
        graphics_and_design_members_count = len(graphics_and_design_members)
        graphics_and_design_members = ",    ".join(sorted(graphics_and_design_members))

        operational_technologist_members = list(
            Profile.objects.all().filter(professional_skill="Operational Technologist"))
        operational_technologist_members = [x.full_name for x in operational_technologist_members]
        operational_technologist_members_count = len(operational_technologist_members)
        operational_technologist_members = ",    ".join(sorted(operational_technologist_members))

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
        return super().get_context_data(**kwargs)
