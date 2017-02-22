from django.conf.urls import url

from .views import SignupView, ThanksView, KeyMachineView

app_name = 'users'
urlpatterns = [
    url(r'^signup/?$', SignupView.as_view(), name='signup'),
    url(r'^thanks/?$', ThanksView.as_view(), name='thanks'),
    url(r'^keymachine/?$', KeyMachineView.as_view(), name='keymachine'),
]
