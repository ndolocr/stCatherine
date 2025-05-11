from django.shortcuts import render

from audit_trail.models import StaffTypeAuditTrail
# Create your views here.

def view_audit_for_staff_type(request, id):
    print("=================================================")
    print(f"Audit Trail -- > Fecth")
    print("=================================================")
    try:
        records = StaffTypeAuditTrail.objects.filter(staff_type = id).order_by('-created_on')
        if records:
            print("=================================================")
            print(f"Record -- > {records}")
            print("=================================================")
            context = {"records": records}            
        else:
            context = {"error_message": "No Audit Trail for record"}
    except Exception as e:
        print("=================================================")
        print(f"Error Occured while retrieving Audit Trail -- > {e}")
        print("=================================================")
        context = {"error_message": "Error Experienced fetching Audit Trail record"}
    return render(request, 'audit_trail/view_audit.html', context)