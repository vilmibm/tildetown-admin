from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Townie, Pubkey

admin.site.unregister(User)
admin.site.unregister(Group)

class PubkeyInline(admin.TabularInline):
    model = Pubkey

def bulk_review(madmin, req, qs):
    for townie in qs:
        townie.reviewed = True
        townie.save()

bulk_review.short_description = 'mark selected townies as reviewed'

@admin.register(Townie)
class TownieAdmin(admin.ModelAdmin):
    inlines = [PubkeyInline]
    list_display = ('reviewed', 'username', 'email')
    ordering = ('reviewed',)
    actions = (bulk_review,)
