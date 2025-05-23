from django.urls import path

from staff import views

app_name = 'staff'

urlpatterns = [
    path('', views.view_all, name='view-all'),
    path('create/', views.create_staff, name='create'),
    path('view/<int:id>', views.view_staff, name='view-staff'),
    path('activate/<int:id>', views.activate_staff, name='activate'),
    path('deactivate/<int:id>', views.deactivate_staff, name='deactivate'),
    path('type', views.view_all_staff_type, name='view-all-staff-type'),
    path('type/create', views.create_staff_type, name='create-staff-type'),
    path('type/update/<int:id>', views.update_staff_type, name='update-staff-type'),
    path('type/delete/<int:id>', views.delete_staff_type, name='delete-staff-type'),
    
    
]