from django.conf.urls import url

from .views import UserSignupView

app_name = 'users'
urlpatterns = [
        url(r'^signup/?$', UserSignupView.as_view(), name='signup'),

]
