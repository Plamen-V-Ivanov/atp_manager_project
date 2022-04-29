import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

# Create your views here.
from atp_manager.auth_app.models import Profile
from atp_manager.web.forms import CreateTaskForm, EditTaskForm, DeleteTaskForm
from atp_manager.web.models import Task


class CreateTaskView(views.CreateView):
    template_name = 'web/add-task.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditTaskView(views.UpdateView):
    model = Task
    template_name = 'web/edit-task.html'
    form_class = EditTaskForm

    def get_success_url(self):
        return reverse('dashboard')

    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         object = self.get_object()
    #         url = object.get_absolute_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(EditTaskView, self).post(request, *args, **kwargs)


class DeleteTaskView(views.DeleteView):
    model = Task
    template_name = 'web/delete-task.html'
    form_class = DeleteTaskForm

    def get_success_url(self):
        return reverse('dashboard')


@login_required
def approve_task_is_done(request, pk):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.is_approved_finished = True
        task.date_finished = datetime.datetime.now()
        task.save()
    return redirect('show closed tasks')


@login_required
def dont_approve_task_is_done(request, pk):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.is_closed_for_approval = False
        task.save()
    return redirect('show closed tasks')


@login_required
def drop_out_the_task(request, pk):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.is_outstanding = True
        task.save()
    return redirect('show requested tasks')


@login_required
def give_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(pk=pk)
        profile = Profile.objects.get(pk=task.is_wanted_by)

        task.taken_by.add(profile)  # ?????????#
        # task.is_taken = True
        task.save()
    return redirect('show requested tasks')


@login_required
def dont_give_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(pk=pk)
        # task.is_wanted = True
        task.is_wanted_by = None
        task.save()
    return redirect('show requested tasks')


@login_required
def take_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(pk=pk)
        # task.is_wanted = True
        task.is_wanted_by = request.user.id
        task.save()
    return redirect('index')


@login_required
def close_task(request, pk):
    if request.user.is_authenticated:
        # if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.is_closed_for_approval = True
        task.save()
    return redirect('index')
