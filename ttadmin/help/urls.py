from django.conf.urls import url

from .views import TicketView, TicketSubmittedView

app_name = 'help'
urlpatterns = [
    url(r'^tickets/?$', TicketView.as_view(), name='tickets'),
    url(r'^tickets/submitted/?$', TicketSubmittedView.as_view(), name='ticket_submitted'),
]
