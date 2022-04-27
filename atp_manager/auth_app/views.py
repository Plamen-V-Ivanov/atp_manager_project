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
        unfinished_tasks = len(profile_tasks.filter(is_approved_finished=True).filter(is_closed_for_approval=True))
        total_tasks = easy_tasks_finished + medium_tasks_finished + hard_tasks_finished + \
                      advanced_tasks_finished + unfinished_tasks
        completed_tasks = total_tasks - unfinished_tasks
        if total_tasks + unfinished_tasks == 0:
            finish_rate = f"{0:.2f}"
        else:
            finish_rate = f"{(completed_tasks / total_tasks) * 100:.2f}"

        context.update({
            'easy_tasks_finished': easy_tasks_finished,
            'medium_tasks_finished': medium_tasks_finished,
            'hard_tasks_finished': hard_tasks_finished,
            'advanced_tasks_finished': advanced_tasks_finished,
            'unfinished_tasks': unfinished_tasks,
            'total_tasks': total_tasks,
            'finish_rate': finish_rate,
            'completed_tasks': completed_tasks,
        })

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # self.object is a Profile instance
    #     pets = list(Pet.objects.filter(user_id=self.object.user_id))
    #
    #     pet_photos = PetPhoto.objects \
    #         .filter(tagged_pets__in=pets) \
    #         .distinct()
    #
    #     total_likes_count = sum(pp.likes for pp in pet_photos)
    #     total_pet_photos_count = len(pet_photos)
    #
    #     context.update({
    #         'total_likes_count': total_likes_count,
    #         'total_pet_photos_count': total_pet_photos_count,
    #         'is_owner': self.object.user_id == self.request.user.id,
    #         'pets': pets,
    #     })
    #
    #     return context


# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     # self.object is a Profile instance
#     # tasks = list(Task.objects.filter(user_id=self.object.user_id))
#
#
#     return context


# def delete_profile(request):
#     return profile_action(request, DeleteProfileForm, 'index', get_profile(), 'main/profile_delete.html')

# class DeleteProfileView(views.DeleteView):
#     form_class = DeleteProfileForm
#     model = Profile
#     template_name = 'profile/delete-member.html'
#     success_url = reverse_lazy('dashboard')

# class DeleteProfileView(views.DeleteView):
#     form_class = DeleteProfileForm
#     model = Profile
#     template_name = 'profile/delete-member.html'
#     success_url = reverse_lazy('dashboard')
#
#     def form_valid(self, form):
#         success_url = self.get_success_url()
#         # form.update()
#         # user_pk = form.instance.pk
#         # user_pk = self.kwargs.get('pk')
#
#         profile = Profile.objects.get(pk=self.kwargs['pk'])
#         profile.delete()
#         return redirect(success_url)
#
#     def get_object(self, queryset=None):
#         pk = self.request.POST['pk']
#         return self.get_queryset().filter(pk=pk).get()


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


# @login_required
# def choose_profile_to_delete(request):
#     pk = 1
#     form_class = ListProfilesForm
#     model = Profile
#     template_name = 'profile/delete-member.html'
#
#     return redirect('delete a profile', pk)


def logout_user(request):
    logout(request)
    return redirect('index')
