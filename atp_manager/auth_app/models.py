import datetime

from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

from django.contrib.auth import models as auth_models

from atp_manager.auth_app.managers import AtpManagerUserManager
from atp_manager.common.validators.validators import validate_only_letters_first_is_capital, \
    validate_only_letters_and_dots_as_separators


class AtpManagerUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25
    USERNAME_MIN_LEN = 6

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            validate_only_letters_and_dots_as_separators,
            MinLengthValidator(USERNAME_MIN_LEN),
        ),
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = AtpManagerUserManager()


class Profile(models.Model):
    AUTOMATION_ENGINEERING = "Automation Engineering"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    GRAPHICS_AMD_DESIGN = "Graphics and Design"
    OPERATIONAL_TECHNOLOGIST = "Operational Technologist"

    SKILLS = [(x, x) for x in (
        AUTOMATION_ENGINEERING, ELECTRICAL_ENGINEERING, MECHANICAL_ENGINEERING, GRAPHICS_AMD_DESIGN,
        OPERATIONAL_TECHNOLOGIST
    )]

    MALE = "Male"
    FEMALE = "Female"
    GENDERS = [(x, x) for x in (MALE, FEMALE)]

    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MAX_LEN = 30
    FIRST_NAME_MIN_LEN = 2
    LAST_NAME_MIN_LEN = 2

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        verbose_name="First Name",
        validators=(
            validate_only_letters_first_is_capital,
            MinLengthValidator(LAST_NAME_MIN_LEN),

        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        verbose_name="Last name",
        validators=(
            validate_only_letters_first_is_capital,
            MinLengthValidator(LAST_NAME_MIN_LEN),
        )
    )

    email = models.EmailField(
        verbose_name="Email",
    )

    picture = models.URLField(
        verbose_name="Picture",
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        verbose_name="Date Of Birth",
    )

    professional_skill = models.CharField(
        max_length=max(len(x) for (x, _) in SKILLS),
        verbose_name="Professional Skill",
        choices=SKILLS,
    )

    gender = models.CharField(
        max_length=max(len(x) for (x, _) in GENDERS),
        choices=GENDERS,
    )

    joined_the_team = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.OneToOneField(
        AtpManagerUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def date_joined_the_team(self):
        return self.joined_the_team.date()

    def __str__(self):
        return f'{self.first_name} {self.last_name} : {self.professional_skill}'
