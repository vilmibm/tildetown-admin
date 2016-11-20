from django.contrib import admin
from .models import Townie

@admin.register(Townie)
class TownieAdmin(admin.ModelAdmin):
    pass
