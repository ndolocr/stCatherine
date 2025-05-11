from django.urls import path

from audit_trail import views

app_name = 'audit'

urlpatterns = [
    path('staff/type/<int:id>', views.view_audit_for_staff_type, name='view-audit-for-staff-type'),
]