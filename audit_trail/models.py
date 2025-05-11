from django.db import models

from staff.models import StaffType
from user_management.models import User

# Create your models here.

class StaffTypeAuditTrail(models.Model):
    class Meta:
        db_table = 'staff_type_audit_trail'
        
    description = models.TextField(blank=False, null=False)
    action = models.CharField(max_length=255, blank=False, null=False)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_by', blank=False, null=False)
    staff_type = models.ForeignKey(StaffType, on_delete=models.CASCADE, related_name='staff_type', blank=False, null=False)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)