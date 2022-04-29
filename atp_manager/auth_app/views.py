from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import redirect

# Create your views here.


from django.views import generic as views
from django.contrib.auth import views as auth_views, logout
from django.urls import reverse_lazy

from atp_manager.auth_app.forms import CreateProfileForm, DeleteProfileForm
from atp_manager.auth_app.models import Profile

from atp_manager.web.models import Task


class AddProfileView(PermissionRequiredMixin, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'profile/add-member.html'
    permission_required = 'auth_app.add_profile'
    success_url = reverse_lazy('dashboard')


class UserLoginView(auth_views.LoginView):
    template_name = 'profile/login-page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'profile/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_tasks = Task.objects.all().filter(taken_by__user_id=self.object.user_id)
        easy_tasks_finished = len(profile_tasks.filter(difficulty="Easy").filter(is_approved_finished=True))
        medium_tasks_finished = len(profile_tasks.filter(difficulty="Medium").filter(is_approved_finished=True))
        hard_tasks_finished = len(profile_tasks.filter(difficulty="Hard").filter(is_approved_finished=True))
        advanced_tasks_finished = len(profile_tasks.filter(difficulty="Advanced").filter(is_approved_finished=True))
        outstanding_tasks = len(profile_tasks.filter(is_outstanding=True))
        total_tasks = easy_tasks_finished + medium_tasks_finished + hard_tasks_finished + \
                      advanced_tasks_finished + outstanding_tasks
        completed_tasks = total_tasks - outstanding_tasks
        if total_tasks == 0:
            finish_rate = f"{0:.2f}"
        else:
            finish_rate = f"{(completed_tasks / total_tasks) * 100:.2f}"

        context.update({
            'easy_tasks_finished': easy_tasks_finished,
            'medium_tasks_finished': medium_tasks_finished,
            'hard_tasks_finished': hard_tasks_finished,
            'advanced_tasks_finished': advanced_tasks_finished,
            'outstanding_tasks': outstanding_tasks,
            'total_tasks': total_tasks,
            'finish_rate': finish_rate,
            'completed_tasks': completed_tasks,
        })

        return context


class DeleteProfileFormView(views.FormView, LoginRequiredMixin):
    form_class = DeleteProfileForm
    model = Profile
    template_name = 'profile/delete-member.html'
    success_url = 'dashboard'

    def form_valid(self, form):
        profiles = form.cleaned_data['profiles'].pk
        profile = Profile.objects.get(pk=profiles)
        profile.delete()
        return redirect(self.success_url)


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()


def logout_user(request):
    logout(request)
    return redirect('index')
