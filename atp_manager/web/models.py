import datetime

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from atp_manager.auth_app.models import AtpManagerUser, Profile

UserModel = get_user_model()


# -----------------------------------------------------

class Task(models.Model):
    AUTOMATION_ENGINEERING = "Automation Engineering"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    GRAPHICS_AMD_DESIGN = "Graphics and Design"
    OPERATIONAL_TECHNOLOGIST = "Operational Technologist"

    SKILLS = [(x, x) for x in (
        AUTOMATION_ENGINEERING, ELECTRICAL_ENGINEERING, MECHANICAL_ENGINEERING, GRAPHICS_AMD_DESIGN,
        OPERATIONAL_TECHNOLOGIST
    )]

    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    ADVANCED = "Advanced"

    DIFFICULTIES = [(x, x) for x in (EASY, MEDIUM, HARD, ADVANCED)]

    TITLE_MAX_LEN = 200

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        verbose_name="Title",
        # validators=(
        #
        # )
    )

    description = models.TextField(
        verbose_name="Description",
    )

    category = models.TextField(
        max_length=max(len(x) for (x, _) in SKILLS),
        verbose_name="Category",
        choices=SKILLS,
    )

    difficulty = models.TextField(
        max_length=max(len(x) for (x, _) in DIFFICULTIES),
        verbose_name="Difficulty",
        choices=DIFFICULTIES,
    )

    is_approved_finished = models.BooleanField(
        default=False,
    )

    is_closed_for_approval = models.BooleanField(
        default=False,
    )

    is_outstanding = models.BooleanField(
        default=False,
    )

    date_added = models.DateField(
        auto_now_add=True,
    )

    taken_by = models.ManyToManyField(
        Profile,
        blank=True,

    )

    date_finished = models.DateField(
        blank=True,
        null=True,
    )

    taken_by_names = models.TextField(
        default="None",
        blank=True,
    )

    is_wanted_by = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title} : {self.category}'

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('date_added', 'title',)
