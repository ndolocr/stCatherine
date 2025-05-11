from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from audit_trail.models import StaffAuditTrail
from audit_trail.models import StaffTypeAuditTrail

from staff.models import StaffType
# Create your views here.

@login_required(login_url='login')
def view_audit_for_all_staff_type(request):
    try:
        records = StaffTypeAuditTrail.objects.all().order_by('created_on')
        if records:
            print("=================================================")
            print(f"Record -- > {records}")
            print("=================================================")
            context = {                
                "records": records,
                "staff_open":"open",
                "staff_active":"active",
                "staff_type_open":"open",
                "app_name": "Staff Type",
                "staff_type_active":"active",
            }
        else:
            context = {"error_message": "No Audit Trail for record"}
    except Exception as e:
        print("=================================================")
        print(f"Error Occured while retrieving Audit Trail -- > {e}")
        print("=================================================")
        context = {
            "staff_open":"open",
            "staff_active":"active",
            "staff_type_open":"open",
            "staff_type_active":"active",
            "error_message": "Error Experienced fetching Audit Trail record"
        }
    return render(request, 'audit_trail/view_all.html', context)

@login_required(login_url='login')
def view_audit_for_staff_type(request, id):
    print("=================================================")
    print(f"Audit Trail -- > Fecth")
    print("=================================================")
    try:
        records = StaffTypeAuditTrail.objects.filter(staff_type = id).order_by('-created_on')
        staff_type = StaffType.objects.get(id=id)

        if records:
            print("=================================================")
            print(f"Record -- > {records}")
            print("=================================================")
            context = {
                "records": records,
                "staff_open":"open",                
                "staff_active":"active",
                "staff_type_open":"open",
                "staff_type": staff_type,
                "staff_type_active":"active",
            }
        else:
            context = {"error_message": "No Audit Trail for record"}
    except Exception as e:
        print("=================================================")
        print(f"Error Occured while retrieving Audit Trail -- > {e}")
        print("=================================================")
        context = {
            "staff_open":"open",
            "staff_active":"active",
            "staff_type_open":"open",
            "staff_type_active":"active",
            "error_message": "Error Experienced fetching Audit Trail record"
        }
    return render(request, 'audit_trail/view_audit.html', context)

@login_required(login_url='login')
def view_audit_for_all_staff(request):
    try:
        records = StaffAuditTrail.objects.all().order_by('-created_on')
        if records:
            print("=================================================")
            print(f"Record -- > {records}")
            print("=================================================")
            context = {                
                "records": records,
                "staff_open":"open",
                "app_name": "Staff",
                "staff_active":"active",
                "staff_type_open":"open",                
                "staff_type_active":"active",
            }
        else:
            context = {"error_message": "No Audit Trail for record"}
    except Exception as e:
        print("=================================================")
        print(f"Error Occured while retrieving Audit Trail -- > {e}")
        print("=================================================")
        context = {
            "staff_open":"open",
            "app_name": "Staff",
            "staff_active":"active",
            "staff_type_open":"open",
            "staff_type_active":"active",
            "error_message": "Error Experienced fetching Audit Trail record"
        }
    return render(request, 'audit_trail/view_all.html', context)