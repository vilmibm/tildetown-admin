from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^help/', include('help.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^guestbook/', include('guestbook.urls')),
    url(r'^admin/', admin.site.urls),
]
