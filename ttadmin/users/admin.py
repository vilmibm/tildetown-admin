from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Townie

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Townie)
class TownieAdmin(admin.ModelAdmin):
    pass
