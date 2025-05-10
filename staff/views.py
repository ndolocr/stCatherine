from datetime import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from staff.models import StaffType
from audit_trail.models import StaffTypeAuditTrail

from utils.form_validation import validate_name

# Create your views here.
@login_required(login_url='login')
def view_all_staff_type(request):
    try:
        records = StaffType.objects.all()

        context = {
            "records": records,
            "title": "Staff Type",
            "subtitle": "View All",
            "staff_type_open":"open",
            "staff_type_active":"active",
        }
    except Exception as e:
        context = {
            "title": "Staff Type",
            "subtitle": "View All",
            "staff_type_open":"open",
            "staff_type_active":"active",
            "error_message": "Unable to retrieve Staff Type records!"
        }

    return render(request, 'staff/view_all_staff_type.html', context)

@login_required(login_url='login')
def create_staff_type(request):
    if request.method == "GET":
        context = {
            "title": "Staff Type",
            "subtitle": "Create",
            "staff_type_open":"open",
            "staff_type_active":"active",
        }
        return render(request, "staff/create_staff_type.html", context)
    elif request.method == "POST":
        name = request.POST.get('name', None)

        print("=================================================")
        print("Captured Data!")
        print("=================================================")
        print(f"Name -- > {name}")

        print("=================================================")
        print("Data Validation Results!")
        print("=================================================")
        print(f"Email Validation --> {validate_name(name)}")
        
        if not name or not validate_name(name):
            context = {
                "title": "Staff Type",
                "subtitle": "Create",
                "staff_type_open":"open",
                "staff_type_active":"active",
                "error_message": "Invalid Staff Type Name!"
            }
            return render(request, 'staff/create_staff_type.html', context)
                
        try:
            # Saving Staff Type record
            staff_type = StaffType.objects.create(name = name,created_by = request.user)
            try:
                # Saving Audit Trail
                audit_trial = StaffTypeAuditTrail.objects.create(
                    action = "Create",
                    staff_type = staff_type,
                    action_by = request.user,
                    description = f"Staff Type Record with name {name} created by {request.user} on {datetime.now()}"
                )
            except Exception as e:
                context = {
                    "title": "Staff Type",
                    "subtitle": "Create",
                    "staff_type_open":"open",
                    "staff_type_active":"active",
                    "error_message": "Error experinced while saving Audit Trail for Staff Type"
                }
                return render(request, "staff/create_staff_type.html", context)
        except Exception as e:
            context = {
                "title": "Staff Type",
                "subtitle": "Create",
                "staff_type_open":"open",
                "staff_type_active":"active",
                "error_message": "Error experinced while saving Staff Type Record"
            }
            return render(request, "staff/create_staff_type.html", context)



        return redirect('staff:view-all-staff-type')

@login_required(login_url='login')
def update_staff_type(request, id):
    context = {
            "title": "Staff Type",
            "subtitle": "Update",
            "staff_type_open":"open",
            "staff_type_active":"active",
        }
    if request.method == "GET":        
        record = get_staff_type_record(id)
        if record:
            print(f"RECORD GOT -----> {record}")
            context["record"]= record                
        else:   
            print(f"RECORD NOT FOUND -----> {record}")         
            context["error_message"]= f"Record with ID ({id}) NOT FOUND"
        return render(request, 'staff/update_staff_type.html', context)
    
    elif request.method =="POST":
        record = get_staff_type_record(id)
        if record:
            name = request.POST.get('name', None)

            print("=================================================")
            print("Captured Data!")
            print("=================================================")
            print(f"Name -- > {name}")

            print("=================================================")
            print("Data Validation Results!")
            print("=================================================")
            print(f"Email Validation --> {validate_name(name)}")
        
            if not name or not validate_name(name):
                context = {
                    "title": "Staff Type",
                    "subtitle": "Create",
                    "staff_type_open":"open",
                    "staff_type_active":"active",
                    "error_message": "Invalid Staff Type Name!"
                }
                return render(request, 'staff/update_staff_type.html', context)
        
            # Update Staff Type
            record.name = name
            record.save()
        
            return redirect('staff:view-all-staff-type')
        else:
            print(f"RECORD NOT FOUND -----> {record}")         
            context["error_message"]= f"Record with ID ({id}) NOT FOUND"
            return render(request, 'staff/update_staff_type.html', context)


def get_staff_type_record(id):
    try:
        record  = StaffType.objects.get(id=id)
        print("=================================================")
        print(f"Record --> {record}!")
        print(f"Record Name --> {record.name}!")
        print("=================================================")
        return record        
    except Exception as e:
        print("=================================================")
        print(f"Error getting record --> {e}!")
        print("=================================================")
        return False