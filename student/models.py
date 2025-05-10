from django.db import models

from user_management.models import User
# Create your models here.
class Student(models.Model):  
    class Meta:
        db_table = 'student'
          
    admitted_on = models.DateField(blank=True, null=True)
    admission_number = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_created_by')
        