from django.urls import path

from audit_trail import views

app_name = 'audit'

urlpatterns = [
    path('staff/view/all', views.view_audit_for_all_staff, name='view-audit-for-all-staff'),    
    path('staff/type/<int:id>', views.view_audit_for_staff_type, name='view-audit-for-staff-type'),

    path('staff/view/<int:id>', views.view_audit_for_single_staff, name='view-audit-for-single-staff'),
    path('staff/type/view/all', views.view_audit_for_all_staff_type, name='view-audit-for-all-staff-type'),
]