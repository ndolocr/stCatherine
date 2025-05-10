from django.db import models

# Create your models here.

class student_level(models.Model):
    class Meta:
        db_table = 'class'    

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # created_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='created_by')