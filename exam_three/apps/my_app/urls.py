from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),  #To capture user input into database THEN redirect to back to root so user can LOGIN
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^add_to_favs/(?P<id>\d+)$', views.add_to_favs),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^remove_from_favs/(?P<id>\d+)$', views.remove_from_favs),
    url(r'^login$', views.login),  #To go through login procedure and EITHER REDIRECT if errors, OR render dashboard HTML page
    url(r'^logout', views.logout),  #To go thru logout procedure to clear session and REDIRECT user to root
]