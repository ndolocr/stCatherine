from django.db import models

from user_management.models import User
from student_level.models import StudentLevel

# Create your models here.
class Stream(models.Model):
    class Meta:
        db_table = 'stream'    

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    student_level = models.ForeignKey(StudentLevel, on_delete=models.CASCADE, related_name='class')