from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Townie, Pubkey

admin.site.unregister(User)
admin.site.unregister(Group)

class PubkeyInline(admin.TabularInline):
    model = Pubkey

@admin.register(Townie)
class TownieAdmin(admin.ModelAdmin):
    inlines = [PubkeyInline]
    list_display = ('reviewed', 'username', 'email')
    ordering = ('reviewed',)
