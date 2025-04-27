from django.contrib import admin
from .models import Invite, UserProfile

# Register your models here.
@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class InviteAdmin(admin.ModelAdmin):
    pass