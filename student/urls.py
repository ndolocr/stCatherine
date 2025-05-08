from django.urls import path

from student import views

app_name = 'student'

urlpatterns = [
    path('create/', views.create, name = 'create'),
]