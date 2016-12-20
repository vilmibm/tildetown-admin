from django.conf.urls import url

from .views import GuestbookView

app_name = 'guestbook'
urlpatterns = [
    url(r'^$', GuestbookView.as_view(), name='guestbook'),
]
