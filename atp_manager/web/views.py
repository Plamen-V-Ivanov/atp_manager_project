from django.shortcuts import render


# Create your views here.

def get_profile():
    profile = 1
    # profile = None
    return profile


def show_index(request):
    profile = get_profile()

    if profile:
        context = {
            'profile': profile,
            'profile.pk': 1
        }

        return render(request, 'home-with-profile.html', context)
    else:
        return render(request, 'home-no-profile.html')


def show_profile(request, pk):
    profile = get_profile()
    context = {
        'profile': profile,
    }
    return render(request, 'profile-details.html', context)


def show_profile_tasks(request, pk):
    profile = get_profile()
    context = {
        'profile': profile,
    }
    return render(request, 'profile-tasks.html', context)


def show_available_tasks(request):
    return render(request, 'available-tasks.html')


def show_running_tasks(request):
    return render(request, 'running-tasks.html')


def suggest_a_task(request):
    return render(request, 'suggest-task.html')

def add_a_note(request):
    return render(request, 'add-note.html')


def show_team(request):
    return render(request, 'team-details.html')


"""

class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class DashboardView(views.ListView):
    model = PetPhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'pet_photos'

class PetPhotoDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = PetPhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'pet_photo'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        viewed_pet_photos = request.session.get('last_viewed_pet_photo_ids', [])

        viewed_pet_photos.insert(0, self.kwargs['pk'])
        request.session['last_viewed_pet_photo_ids'] = viewed_pet_photos[:4]

        return response

    def get_queryset(self):
        return super() \
            .get_queryset() \
            .prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.user == self.request.user

        return context


class CreatePetPhotoView(auth_mixin.LoginRequiredMixin, views.CreateView):
    model = PetPhoto
    template_name = 'main/photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')

    success_url = reverse_lazy('dashboard')

    # def get_queryset(self):
    #     # .filter(user=self.request.user)
    #     pass

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPetPhotoView(views.UpdateView):
    model = PetPhoto
    template_name = 'main/photo_edit.html'
    fields = ('description',)

    def get_success_url(self):
        return reverse_lazy('pet photo details', kwargs={'pk': self.object.id})


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()

    return redirect('pet photo details', pk)
    
        


class CreatePetView(views.CreateView):
    template_name = 'main/pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPetView(views.UpdateView):
    template_name = 'main/pet_edit.html'
    form_class = EditPetForm


class DeletePetView(views.DeleteView):
    template_name = 'main/pet_delete.html'
    form_class = DeletePetForm   
    
    
    
    
    
    
"""