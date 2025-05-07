from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('logout', views.logout, name='logout'),
]