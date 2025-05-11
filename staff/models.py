from django.db import models

from user_management.models import User

# Create your models here.

class StaffType(models.Model):
    class Meta:
        db_table = 'staff_type'

    deleted_status = models.BooleanField(default=False)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_type_created_by', blank=False, null=False)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    class Meta:
        db_table = 'staff'
    
    date_joined = models.DateField(blank=True, null=True)
    id_number = models.CharField(max_length=255, blank=True, null=True)  
    staff_number = models.CharField(max_length=255, blank=True, null=True)
    staff_types = models.ManyToManyField(StaffType, related_name='staff_type_members')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_created_by', blank=False, null=False)

    def __str__(self):
        return self.user.first_name