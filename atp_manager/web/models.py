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

    # DAY_ONE = "1 Day"
    # DAYS_THREE = "3 Day"
    # WEEK_ONE = "1 Week"
    # WEEKS_TWO = "2 Week"
    # MONTH_ONE = "1 Month"
    # MONTHS_THREE = "3 Month"
    # MONTHS_SIX = "6 Month"
    # YEAR = "a Year"
    #
    # EXPIRATION_TIMES = [(x, x) for x in (
    #     DAY_ONE, DAYS_THREE, WEEK_ONE, WEEKS_TWO, MONTH_ONE, MONTHS_THREE, MONTHS_SIX, YEAR
    # )]

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

    # expiration_time = models.TextField(
    #     max_length=max(len(x) for (x, _) in EXPIRATION_TIMES),
    #     verbose_name="Expiration Time",
    #     choices=EXPIRATION_TIMES,
    # )

    # is_taken = models.BooleanField(
    #     default=False,
    # )

    is_approved_finished = models.BooleanField(
        default=False,
    )

    is_closed_for_approval = models.BooleanField(
        default=False,
    )

    is_wanted = models.BooleanField(
        default=False,
    )

    # is_suggested = models.BooleanField(
    #     default=False,
    # )

    date_added = models.DateField(
        auto_now=True,
    )

    # expire_time_in_hours = models.IntegerField(
    #     default=0,
    # )

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

    # @property
    # def get_people_involved(self):
    #     people = self.taken_by
    #     return people

    '''
    Explanation:
    Set expire date when someone get the task (is_occupied == TRUE)
    '''

    # @property
    # def calculate_expire_time_in_hours(self):
    #     expire_time = None
    #     expire_time_in_hours_dict = {
    #         "1 Day": 24,
    #         "3 Day": 3 * 24,
    #         "1 Week": 7 * 24,
    #         "2 Week": 2 * 7 * 24,
    #         "1 Month": 30 * 24,
    #         "3 Month": 3 * 30 * 24,
    #         "6 Month": 6 * 30 * 24,
    #         "a Year": 12 * 30 * 24,
    #     }
    #
    #     if self.is_taken:
    #         expire_time = datetime.datetime.now().hour + expire_time_in_hours_dict[self.expiration_time]
    #     return expire_time

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('date_added', 'title',)


# class WebPageSetting(models.Model):
#     DEFAULT_MESSAGE = 'Optimize The World!'
#     # DEFAULT_AUTOMATION_ENGINEERING_IMAGE_URL = '/static/images/wp3610487.jpg'
#     # DEFAULT_MECHANICAL_ENGINEERING_IMAGE_URL = '/static/images/546188.jpg'
#     # DEFAULT_ELECTRICAL_ENGINEERING_IMAGE_URL = '/static/images/eng-2.png'
#     # DEFAULT_GRAPHICS_AND_DESIGN_IMAGE_URL = '/static/images/design-line-graphic-design-graphics-wallpaper-preview.jpg'
#     # DEFAULT_OPERATIONAL_TECHNOLOGIST_IMAGE_URL = '/static/images/1880092.jpg'
#
#     WellcomeMessage = models.TextField(
#         default=DEFAULT_MESSAGE
#     )
#
#     automation_engineering_image = models.URLField(
#         # default=DEFAULT_AUTOMATION_ENGINEERING_IMAGE_URL,
#         blank=True,
#         null=True,
#
#     )
#
#     electrical_engineering_image = models.URLField(
#         # default=DEFAULT_ELECTRICAL_ENGINEERING_IMAGE_URL,
#         blank=True,
#         null=True,
#     )
#
#     mechanical_engineering_image = models.URLField(
#         # default=DEFAULT_MECHANICAL_ENGINEERING_IMAGE_URL,
#         blank=True,
#         null=True,
#     )
#
#     graphics_and_design_image = models.URLField(
#         # default=DEFAULT_GRAPHICS_AND_DESIGN_IMAGE_URL,
#         blank=True,
#         null=True,
#     )
#
#     operational_technologist_image = models.URLField(
#         # default=DEFAULT_OPERATIONAL_TECHNOLOGIST_IMAGE_URL,
#         blank=True,
#         null=True,
#     )


# class TeamStats(models.Model):
#     automation_tasks = models.IntegerField(default=0)
#     mechanical_tasks = models.IntegerField(default=0)
#     electrical_tasks = models.IntegerField(default=0)
#     graphics_and_design_tasks = models.IntegerField(default=0)
#     operational_tasks = models.IntegerField(default=0)
#     outstanding_tasks = models.IntegerField(default=0)
#
#     @property
#     def total_tasks(self):
#         total_tasks = self.automation_tasks + self.mechanical_tasks + self.electrical_tasks + \
#                       self.graphics_and_design_tasks + self.operational_tasks + \
#                       self.operational_tasks
#         return total_tasks


'''
TO DO:
Make validators for name - only letters
'''

'''
MAYBE:
Remove OTHER IN CATEGORIES
'''

'''
MAYBE:
Change SKILLS TO CATEGORIES - its better that way
'''
