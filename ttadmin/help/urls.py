from django.conf.urls import url

from .views import TicketView

app_name = 'help'
urlpatterns = [
    url(r'^tickets/?$', TicketView.as_view(), name='tickets'),
]
