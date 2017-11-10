from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Townie, Pubkey
from common.social import post_users_to_social

admin.site.unregister(User)
admin.site.unregister(Group)

class PubkeyInline(admin.TabularInline):
    model = Pubkey
    extra = 1

def mark_reviewed(madmin, req, qs):
    for townie in qs:
        townie.reviewed = True
        townie.save()
    post_users_to_social(qs)

mark_reviewed.short_description = 'mark selected as reviewed'

@admin.register(Townie)
class TownieAdmin(admin.ModelAdmin):
    inlines = [PubkeyInline]
    list_display = ('username', 'reviewed', 'email')
    ordering = ('reviewed',)
    exclude = ('first_name', 'last_name', 'password', 'groups', 'user_permissions', 'last_login')
    actions = (mark_reviewed,)
    search_fields = ('username', 'email', 'displayname')
