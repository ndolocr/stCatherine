from django.urls import path

from student import views

app_name = 'student'

urlpatterns = [
    path('', views.index, name = 'view-all'),
    path('create/', views.create, name = 'create'),
]