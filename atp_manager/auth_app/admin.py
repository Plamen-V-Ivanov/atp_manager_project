from django.contrib import admin

# Register your models here.


from django.contrib import admin

from atp_manager.auth_app.models import Profile, AtpManagerUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (PetInlineAdmin,)
    # list_display = ('first_name', 'last_name')
    pass


@admin.register(AtpManagerUser)
class AtpManagerUserAdmin(admin.ModelAdmin):
    # inlines = (PetInlineAdmin,)
    # list_display = ('first_name', 'last_name')
    pass


# @admin.register(ProfileStat)
# class ProfileStatsAdmin(admin.ModelAdmin):
#     # inlines = (PetInlineAdmin,)
#     # list_display = ('first_name', 'last_name')
#     pass
