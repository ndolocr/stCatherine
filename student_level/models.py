from django.db import models

from user_management.models import User
# Create your models here.

class StudentLevel(models.Model):
    class Meta:
        db_table = 'student_class'    

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_level_created_by')