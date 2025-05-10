from django.shortcuts import render
from django.shortcuts import redirect

from staff.models import StaffType

from utils.form_validation import validate_name

# Create your views here.
def view_all_staff_type(request):
    records = StaffType.objects.all()

    context = {
        "records": records,
        "title": "Staff Type",
        "subtitle": "View All",
        "staff_type_open":"open",
        "staff_type_active":"active",
    }

    return render(request, 'staff/view_all_staff_type.html', context)

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
                "error_message": "Invalid name format Only use WORDS"
            }
            return render(request, 'staff/create_staff_type.html', context)
        
        # Create Staff Type
        staff_type = StaffType.objects.create(
            name = name,
            created_by = request.user,
        )

        return redirect('staff:view-all-staff-type')