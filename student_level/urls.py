from django.urls import path

from student_level import views

app_name="class"

urlpatterns = [
    path('create', views.create, name='create'),
]