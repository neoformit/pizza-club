from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu, name='menu'),
    url('confirm/', views.confirm, name='confirm'),
    url('confirmation/', views.confirmation, name='confirmation'),
    url('cancel/', views.cancel, name='cancel'),
    ]
