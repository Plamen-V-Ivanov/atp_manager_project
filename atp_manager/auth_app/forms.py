from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.validators import MinLengthValidator

from atp_manager.auth_app.models import Profile


# class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
#     first_name = forms.CharField(
#         max_length=Profile.FIRST_NAME_MAX_LEN,
#     )
#     last_name = forms.CharField(
#         max_length=Profile.LAST_NAME_MAX_LEN,
#     )
#     email = forms.EmailField()
#
#     picture = forms.URLField(
#     )
#
#     date_of_birth = forms.DateField()
#
#     professional_skill = forms.ChoiceField(
#         choices=Profile.SKILLS,
#     )
#
#     gender = forms.ChoiceField(
#         choices=Profile.GENDERS,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._init_bootstrap_form_controls()
#
#     def save(self, commit=True):
#         user = super().save(commit=commit)
#
#         profile = Profile(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             picture=self.cleaned_data['picture'],
#             date_of_birth=self.cleaned_data['date_of_birth'],
#             professional_skill=self.cleaned_data['professional_skill'],
#             email=self.cleaned_data['email'],
#             gender=self.cleaned_data['gender'],
#             user=user,
#         )
#
#         if commit:
#             profile.save()
#         return user
#
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'professional_skill')
#         widgets = {
#             'first_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter first name',
#                 }
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter last name',
#                 }
#             ),
#             'picture': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter URL - optional',
#                 }
#             ),
#         }
from atp_manager.common.validators.validators import validate_only_letters_first_is_capital


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LEN,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'First name'}),
        validators=(
            validate_only_letters_first_is_capital,
            MinLengthValidator(Profile.FIRST_NAME_MIN_LEN),
        )
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LEN,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Last name'}),
        validators=(
            validate_only_letters_first_is_capital,
            MinLengthValidator(Profile.LAST_NAME_MIN_LEN),
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Email'}),
    )

    picture = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'picture is optional'}),
    )

    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'YY-MM-DD'}),
    )

    professional_skill = forms.ChoiceField(
        choices=Profile.SKILLS,
    )

    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            professional_skill=self.cleaned_data['professional_skill'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'professional_skill', 'email',
            'date_of_birth', 'gender')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                }
            ),
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        valid_domain = 'atp-bg.com'
        if domain != valid_domain:
            raise forms.ValidationError("Please enter an Email Address with a valid domain '@atp-bg.com'")
        return data



    #
    #
    # class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self._init_bootstrap_form_controls()
    #         self.initial['gender'] = Profile.DO_NOT_SHOW
    #
    #     class Meta:
    #         model = Profile
    #         fields = '__all__'
    #         widgets = {
    #             'first_name': forms.TextInput(
    #                 attrs={
    #                     'placeholder': 'Enter first name',
    #                 }
    #             ),
    #             'last_name': forms.TextInput(
    #                 attrs={
    #                     'placeholder': 'Enter last name',
    #                 }
    #             ),
    #             'picture': forms.TextInput(
    #                 attrs={
    #                     'placeholder': 'Enter URL',
    #                 }
    #             ),
    #             'email': forms.EmailInput(
    #                 attrs={
    #                     'placeholder': 'Enter email',
    #                 }
    #             ),
    #             'description': forms.Textarea(
    #                 attrs={
    #                     'placeholder': 'Enter description',
    #                     'rows': 3,
    #                 },
    #             ),
    #             'date_of_birth': forms.DateInput(
    #                 attrs={
    #                     'min': '1920-01-01',
    #                 }
    #             )
    #         }
    #
    #

    # check how to use signals for delete form in django

    # class DeleteProfileForm(forms.ModelForm):
    #     profiles = forms.ModelChoiceField(
    #         widget=forms.Select,
    #         queryset=Profile.objects.all(),
    #     )  # here you can filter for what choices you need
    #
    #     def save(self, commit=True):
    #         self.instance.delete()
    #         return self.instance
    #
    #     class Meta:
    #         model = Profile
    #         fields = ()

    # class DeleteProfileForm(forms.ModelForm):
    #
    #     def save(self, commit=True):
    #         self.instance.delete()
    #         return self.instance
    #
    #     class Meta:
    #         model = Profile
    #         fields = ()

    # class SelectProfileForm(forms.ModelForm):
    #     profiles = forms.ModelChoiceField(
    #         widget=forms.Select,
    #         queryset=Profile.objects.all(),
    #         # empty_label="----None----",
    #     )  # here you can filter for what choices you need
    #
    #
    #     class Meta:
    #         model = Profile
    #         fields = ()

class DeleteProfileForm(forms.ModelForm):
    profiles = forms.ModelChoiceField(
        widget=forms.Select,
        queryset=Profile.objects.all(),
        # empty_label="----none----",
        label="",
    )  # here you can filter for what choices you need

    class Meta:
        model = Profile
        fields = ()
