from django.contrib import admin
from .models import GuestbookMessage

@admin.register(GuestbookMessage)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime_created', 'msg')
