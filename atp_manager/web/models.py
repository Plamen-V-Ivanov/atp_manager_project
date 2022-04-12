import datetime

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from atp_manager.auth_app.models import AtpManagerUser



UserModel = get_user_model()


# -----------------------------------------------------

class Task(models.Model):

    AUTOMATION = "Automation"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    GRAPHICS_AMD_DESIGN = "Graphics & Design"
    OPERATIONAL = "Operational"
    OTHER = "Other"

    SKILLS = [(x, x) for x in (
        AUTOMATION, ELECTRICAL_ENGINEERING, MECHANICAL_ENGINEERING, GRAPHICS_AMD_DESIGN, OPERATIONAL, OTHER
    )]

    RANK1 = "Rank 1"
    RANK2 = "Rank 2"
    RANK3 = "Rank 3"
    RANK4 = "Rank 4"

    RANKS = [(x, x) for x in (RANK1, RANK2, RANK3, RANK4)]

    DAY_ONE = "1 Day"
    DAYS_THREE = "3 Day"
    WEEK_ONE = "1 Week"
    WEEKS_TWO = "2 Week"
    MONTH_ONE = "1 Month"
    MONTHS_THREE = "3 Month"
    MONTHS_SIX = "6 Month"
    YEAR = "a Year"

    EXPIRATION_TIMES = [(x, x) for x in (
        DAY_ONE, DAYS_THREE, WEEK_ONE, WEEKS_TWO, MONTH_ONE, MONTHS_THREE, MONTHS_SIX, YEAR
    )]

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

    rank = models.TextField(
        max_length=max(len(x) for (x, _) in RANKS),
        verbose_name="Rank",
        choices=RANKS,
    )

    expiration_time = models.TextField(
        max_length=max(len(x) for (x, _) in EXPIRATION_TIMES),
        verbose_name="Expiration Time",
        choices=EXPIRATION_TIMES,
    )

    is_occupied = models.BooleanField(
        default=False,
    )

    is_completed = models.BooleanField(
        default=False,
    )

    is_closed = models.BooleanField(
        default=False,
    )

    is_proposed = models.BooleanField(
        default=False,
    )

    date_added = models.DateField(
        auto_now=True,
    )

    expire_time_in_hours = models.IntegerField(
        default=0,
    )

    '''
    Explanation:
    Set expire date when someone get the task (is_occupied == TRUE)
    '''

    @property
    def calculate_expire_time_in_hours(self):
        expire_time = None
        expire_time_in_hours_dict = {
            "1 Day": 24,
            "3 Day": 3 * 24,
            "1 Week": 7 * 24,
            "2 Week": 2 * 7 * 24,
            "1 Month": 30 * 24,
            "3 Month": 3 * 30 * 24,
            "6 Month": 6 * 30 * 24,
            "a Year": 12 * 30 * 24,
        }

        if self.is_occupied:
            expire_time = datetime.datetime.now().hour + expire_time_in_hours_dict[self.expiration_time]
        return expire_time

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


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
