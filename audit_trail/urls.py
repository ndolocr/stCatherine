from django.urls import path

from audit_trail import views

app_name = 'audit'

urlpatterns = [
    path('staff/type/<int:id>', views.view_audit_for_staff_type, name='view-audit-for-staff-type'),
    path('staff/type/view/all', views.view_audit_for_all_staff_type, name='view-audit-for-all-staff-type'),
]