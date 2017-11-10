from django.contrib import admin
from .models import Ticket

def cycle_state(madmin, req, qs):
    for ticket in qs:
        ticket.cycle_state()
        ticket.save()

cycle_state.short_description = 'move ticket state forward'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    actions = (cycle_state,)
    list_display = ('issue_status', 'issue_type', 'name', 'email')
