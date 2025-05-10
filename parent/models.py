from django.db import models

from student.models import Student
from user_management.models import User

# Create your models here.
class Parent(models.Model):
    class Meta:
        db_table = 'parent'

    children = models.ManyToManyField(Student, related_name='parents')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_created_by')
    