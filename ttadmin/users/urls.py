from django.conf.urls import url

from .views import SignupView, ThanksView

app_name = 'users'
urlpatterns = [
    url(r'^signup/?$', SignupView.as_view(), name='signup'),
    url(r'^thanks/?$', ThanksView.as_view(), name='thanks'),
]
