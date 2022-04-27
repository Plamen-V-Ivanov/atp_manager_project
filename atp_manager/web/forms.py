from django import forms

from atp_manager.common.mixins.mixins import BootstrapFormMixin, DisabledFieldsFormMixin
from atp_manager.web.models import Task


class CreateTaskForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        task = super().save(commit=False)

        # task = Task(
        #     title=self.cleaned_data['title'],
        #     description=self.cleaned_data['description'],
        #     category=self.cleaned_data['category'],
        #     difficulty=self.cleaned_data['difficulty'],
        #     taken_by=self.cleaned_data['taken_by'],
        # )

        task.user = self.user
        if commit:
            task.save()
            self.save_m2m()

        return task

    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'difficulty', 'taken_by')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Title',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter Description',
                    'lines': 3,
                }
            ),
        }


class EditTaskForm(BootstrapFormMixin, forms.ModelForm):
    # MIN_DATE_OF_BIRTH = date(1920, 1, 1)
    # MAX_DATE_OF_BIRTH = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    # def clean_date_of_birth(self):
    #     MaxDateValidator(date.today())(self.cleaned_data['date_of_birth'])
    #     return self.cleaned_data['date_of_birth']

    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'difficulty', 'taken_by')
        # exclude = (
        #     'user_profile', 'taken_by_names', 'is_taken', 'is_wanted', 'is_approved_finished', 'is_suggested',
        #     'is_closed_for_approval', 'user',
        # )


class DeleteTaskForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Task
        exclude = ('user_profile',)
