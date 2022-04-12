import datetime

from django.db import models

# Create your models here.

from django.contrib.auth import models as auth_models

from atp_manager.auth_app.managers import AtpManagerUserManager


class AtpManagerUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
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

    AUTOMATION = "Automation"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    GRAPHICS_AMD_DESIGN = "Graphics & Design"
    OPERATIONAL = "Operational"
    OTHER = "Other"

    SKILLS = [(x, x) for x in (
        AUTOMATION, ELECTRICAL_ENGINEERING, MECHANICAL_ENGINEERING, GRAPHICS_AMD_DESIGN, OPERATIONAL, OTHER
    )]

    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MAX_LEN = 30
    CATEGORY_MAX_LEN = 100

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        verbose_name="First Name",
        # validators=(
        #
        # )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        verbose_name="Last name",
    )

    email = models.EmailField(
        verbose_name="Email",
    )

    image_url = models.URLField(
        verbose_name="Image URL",
    )

    date_of_birth = models.DateField(
        verbose_name="Date Of Birth",
    )

    professional_skill = models.CharField(
        max_length=max(len(x) for (x, _) in SKILLS),
        verbose_name="Professional Skill",
        choices=SKILLS,
    )

    joined_the_team = models.DateTimeField(
        auto_now_add=True,
    )

    rank1_tasks_finished = models.IntegerField(
        default=0,
    )

    rank2_tasks_finished = models.IntegerField(
        default=0,
    )

    rank3_tasks_finished = models.IntegerField(
        default=0,
    )

    rank4_tasks_finished = models.IntegerField(
        default=0,
    )

    tasks_not_finished = models.IntegerField(
        default=0,
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
    def total_finished_tasks(self):
        total = self.rank1_tasks_finished + self.rank2_tasks_finished + \
                self.rank3_tasks_finished + self.rank4_tasks_finished

        return total

    @property
    def finish_rate(self):
        rate = (self.total_finished_tasks / self.total_finished_tasks + self.tasks_not_finished) * 100
        return f'{rate:.2f}'