from datetime import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from staff.models import Staff
from staff.models import StaffType

from user_management.models import User

from audit_trail.models import StaffAuditTrail
from audit_trail.models import StaffTypeAuditTrail

from utils.form_validation import validate_name
from utils.form_validation import validate_email
from utils.form_validation import validate_gender
from utils.form_validation import validate_phone_num

from utils.user_name import generate_unique_username

# Create your views here.
@login_required(login_url='login')
def view_all_staff_type(request):
    try:
        records = StaffType.objects.all().order_by('-created_on')

        context = {
            "records": records,
            "title": "Staff Type",
            "subtitle": "View All",
            "staff_open":"open",
            "staff_active":"active",
            "staff_type_open":"open",
            "staff_type_active":"active",
        }
    except Exception as e:
        context = {
            "title": "Staff Type",
            "subtitle": "View All",
            "staff_open":"open",
            "staff_active":"active",
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
            "staff_open":"open",
            "staff_active":"active",
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
                "staff_open":"open",
                "staff_active":"active",
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
                    description = f"Staff Type Record with name <b>{name}</b> created."
                )
            except Exception as e:
                context = {
                    "title": "Staff Type",
                    "subtitle": "Create",
                    "staff_open":"open",
                    "staff_active":"active",
                    "staff_type_open":"open",
                    "staff_type_active":"active",
                    "error_message": "Error experinced while saving Audit Trail for Staff Type"
                }
                return render(request, "staff/create_staff_type.html", context)
        except Exception as e:
            context = {
                "title": "Staff Type",
                "subtitle": "Create",
                "staff_open":"open",
                "staff_active":"active",
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
            "staff_open":"open",
            "staff_active":"active",
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
            print(f"Name Validation --> {validate_name(name)}")
        
            if not name or not validate_name(name):
                context = {
                    "title": "Staff Type",
                    "subtitle": "Create",
                    "staff_open":"open",
                    "staff_active":"active",
                    "staff_type_open":"open",
                    "staff_type_active":"active",
                    "error_message": "Invalid Staff Type Name!"
                }
                return render(request, 'staff/update_staff_type.html', context)
        
            # Update Staff Type
            original_name = record.name
            print(f"Original Name --> {original_name}")
            record.name = name
            record.save()
            print(f"Saved Name Record --> {record}")
            try:
                # Saving Audit Trail
                audit_trial = StaffTypeAuditTrail.objects.create(
                    action = "Update",
                    staff_type = record,
                    action_by = request.user,
                    description = f"<b>{original_name}</b> updated to <b>{name}</b>"
                )
            except Exception as e:
                context["error_message"]= f"Error saving Audit Trail --> {e}"
                return render(request, 'staff/update_staff_type.html', context)
            return redirect('staff:view-all-staff-type')
        else:
            print(f"RECORD NOT FOUND -----> {record}")         
            context["error_message"]= f"Record with ID ({id}) NOT FOUND"
            return render(request, 'staff/update_staff_type.html', context)

@login_required(login_url='login')
def delete_staff_type(request, id):
    record = get_staff_type_record(id)
    if record:
        record_name = record.name
        record.deleted_status = True
        record.save()
        # record.delete()
        
        # Saving Audit Trail
        audit_trial = StaffTypeAuditTrail.objects.create(
            action = "Delete",
            staff_type = record,
            action_by = request.user,
            description = f"<b>{record_name}</b> deleted successfully!"
        )
        return redirect('staff:view-all-staff-type')

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

# Staff Record
@login_required(login_url='login')
def view_all(request):
    try:
        records = Staff.objects.all().order_by('-date_joined')        

        context = {
            "records": records,
            "title": "Staff",
            "subtitle": "View All",
            "staff_open":"open",
            "staff_active":"active"
        }
    except Exception as e:
        context = {
            "title": "Staff",
            "subtitle": "View All",
            "staff_open":"open",
            "staff_active":"active",
            "error_message": f"Unable to retrieve Staff records -> {e}!"
        }

    return render(request, 'staff/view_all.html', context)
    
@login_required(login_url='login')
def create_staff(request):
    try:
        last_staff_number = Staff.objects.order_by('-id').first()
        new_staff_number = int(last_staff_number.staff_number) + 1
    except Exception as e:
        print("==========================================")
        print(f"Error getting student record to generate next admission number --> {last_staff_number}")
        print("==========================================")
        new_staff_number = 1

        print("==========================================")
        print(f"Last Addmitted student --> {last_staff_number}")
        print(f"Their Admission Number --> {new_staff_number}")
        print("==========================================")

    try:
        staff_type_records = StaffType.objects.all().order_by('name')
    except Exception as e:
        context = {
            "title": "Staff",
            "subtitle": "Create",
            "staff_open":"open",
            "staff_active":"active",
            "error_message": "Staff Type records need to be created first."
        }
        return render(request, "staff/create_staff.html", context)
    
    if request.method =="GET":        
        
        context = {
            "title": "Staff",
            "subtitle": "Create",
            "staff_open":"open",
            "staff_active":"active",
            "new_staff_number": new_staff_number,
            "staff_type_records": staff_type_records
        }
        return render(request, "staff/create_staff.html", context)
    elif request.method =="POST":        
        town = request.POST.get('town', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        about = request.POST.get('about', None)
        gender = request.POST.get('gender', None)
        address = request.POST.get('address', None)
        last_name = request.POST.get('last_name', None)
        first_name = request.POST.get('first_name', None)        
        date_joined = request.POST.get('date_joined', None)
        middle_name = request.POST.get('middle_name', None)
        staff_number = request.POST.get('staff_number', None)
        staff_type = request.POST.getlist('staff_type', None)
        identification_document = request.POST.get('identification_document', None)
        identification_document_number = request.POST.get('identification_document_number', None)

        print("==============================================================")
        print(f"town --> {town}")
        print(f"phone --> {phone}")
        print(f"email --> {email}")
        print(f"about --> {about}")
        print(f"gender --> {gender}")
        print(f"address --> {address}")
        print(f"last_name --> {last_name}")
        print(f"first_name --> {first_name}")
        print(f"staff_type --> {staff_type}")
        print(f"date_joined --> {date_joined}")
        print(f"middle_name --> {middle_name}")
        print(f"staff_number --> {staff_number}")
        print(f"identification_document --> {identification_document}")
        print(f"identification_document_number --> {identification_document_number}")        
        print("==============================================================")
        
        # Validation
        # town
        context = {
            "title": "Staff",
            "subtitle": "Create",
            "staff_open":"open",
            "staff_active":"active",
            "new_staff_number": new_staff_number,
            "staff_type_records": staff_type_records,
        }
        
        if not town or not validate_name(town):
            context["form_error"] = "Invalid town"
            return render(request, "staff/create_staff.html", context)
        
        if not phone:
            context["form_error"] = "Invalid Phone Number. Phone No. should be 12 digits (254 712 345 678)"
            return render(request, "staff/create_staff.html", context)
        
        if not validate_email(email):
            context["form_error"] = "Invalid email"
            return render(request, "staff/create_staff.html", context)
        
        if not gender or not validate_gender(gender):
            context["form_error"] = "Invalid gender"
            return render(request, "staff/create_staff.html", context)
        
        if not last_name or not validate_name(last_name):
            context["form_error"] = "Invalid last name"
            return render(request, "staff/create_staff.html", context)
        
        if not first_name or not validate_name(first_name):
            context["form_error"] = "Invalid first name"
            return render(request, "staff/create_staff.html", context)
        
        if middle_name:
            if not validate_name(middle_name):
                context["form_error"] = "Invalid first name"
                return render(request, "staff/create_staff.html", context)
            
        if not date_joined:
            context["form_error"] = "Employment date required"
            return render(request, "staff/create_staff.html", context)
        
        if not identification_document:
            context["form_error"] = "Identification document required"
            return render(request, "staff/create_staff.html", context)
        
        if not identification_document_number:
            context["form_error"] = "Identification document number required"
            return render(request, "staff/create_staff.html", context)
        
        print("Validation Successful")
        # Create Staff Information
        password = f"({last_name}.{first_name})"
        username = generate_unique_username(first_name, last_name)

        try:
            user = User.objects.create(
                town = town,
                email=email,
                phone=phone,                
                gender=gender,
                is_staff = True,
                is_active = True,
                address = address,
                username=username,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,                
                password=make_password(password),
                identification_document = identification_document,
                identification_document_number = identification_document_number,
                
            )

            staff = Staff.objects.create(
                user = user,
                about=about,
                created_by = request.user,               
                date_joined = date_joined,
                staff_number = staff_number,               
            )
            staff.staff_types.set(staff_type)


            staff_type_names = list(StaffType.objects.filter(id__in=staff_type).values_list('name', flat=True))

            # Create Audit trail for creating staff record
            staff_record = f"""
            <b> <u>Create Staff Record</u> </b> <br>
            Last Name: {last_name}     | Email:{email}         | Phone: {phone}     | Is Active {user.is_active}
            First Name: {first_name}   | Gender: {gender}      | Address: {address} | Is Staff: {user.is_staff}
            Middle Name: {middle_name} | Username: {username}  | Town: {town}
            <br>   
            ID Num: {identification_document_number} |
            ID Doc: {identification_document} |
            Sfatt Type: {staff_type_names} |
            <br>
            <b>About</b> <br>
            {about}
            """
            try:
                audit_trail = StaffAuditTrail.objects.create(
                    staff = staff,
                    action = "Create",
                    action_by = request.user,
                    description = staff_record                
                )
            except Exception as e:
                context = {
                    "title": "Staff",
                    "subtitle": "Create",
                    "staff_open":"open",
                    "staff_active":"active",
                    "new_staff_number": new_staff_number,
                    "staff_type_records": staff_type_records,
                    "form_error": f"Error occured while Audit information. -- {e}"
                }            
            
            return redirect('staff:view-all')
        except Exception as e:
            print("==========================================")
            print(f"The following error occured while saving staff record. --> {e}")
            print("==========================================")
            context = {
                "title": "Staff",
                "subtitle": "Create",
                "staff_open":"open",
                "staff_active":"active",
                "new_staff_number": new_staff_number,
                "staff_type_records": staff_type_records,
                "form_error": "Error occured while saving staff information."
            }

            return render(request, "staff/create_staff.html", context)

@login_required(login_url='login')        
def view_staff(request, id):
    if request.method == "GET":
        record = Staff.objects.get(id=id)
        staff_type_records = StaffType.objects.all()
        assigned_types = record.staff_types.values_list('id', flat=True)

        current_id = id
        next_id = id + 1
        previous_id = id - 1        
        last_user_id = Staff.objects.last().id
        first_user_id = Staff.objects.first().id  

        if previous_id == 0:
            previous_id = first_user_id
        if next_id > last_user_id:
            next_id = last_user_id    
        
        date_joined= record.date_joined.strftime('%Y-%m-%d') if record.date_joined else ''
        
        context = {                     
            "record":record,
            "next_id": next_id,
            "staff_open":"open",
            "staff_active":"active",
            "previous_id": previous_id,
            "date_joined": date_joined,
            "last_user_id": last_user_id,
            "first_user_id": first_user_id,
            "assigned_types": assigned_types,
            "staff_type_records": staff_type_records,
        }
        return render(request, "staff/view_staff.html", context)
    elif request.method == "POST":
        
        town = request.POST.get('town', None)        
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        about = request.POST.get('about', None)
        gender = request.POST.get('gender', None)
        address = request.POST.get('address', None)
        staff_id = request.POST.get('staff_id', None)
        last_name = request.POST.get('last_name', None)
        first_name = request.POST.get('first_name', None)        
        date_joined = request.POST.get('date_joined', None)
        middle_name = request.POST.get('middle_name', None)
        staff_type = request.POST.getlist('staff_type', None)
        identification_document = request.POST.get('identification_document', None)
        identification_document_number = request.POST.get('identification_document_number', None)

        print("==============================================================")
        print(f"town --> {town}")
        print(f"phone --> {phone}")
        print(f"email --> {email}")
        print(f"about --> {about}")
        print(f"gender --> {gender}")
        print(f"address --> {address}")
        print(f"last_name --> {last_name}")
        print(f"first_name --> {first_name}")
        print(f"staff_type --> {staff_type}")
        print(f"date_joined --> {date_joined}")
        print(f"middle_name --> {middle_name}")
        print(f"identification_document --> {identification_document}")
        print(f"identification_document_number --> {identification_document_number}")        
        print("==============================================================")

        staff = Staff.objects.get(id = staff_id)
        print(f"Staff ----> {staff}")
        staff.about = about
        staff.date_joined = date_joined        
        staff.save()

        print("Staff successfully saved")

        staff.staff_types.set(staff_type)
        print("Updating Staff Types")
        
        user_obj = staff.user
        user_obj.town = town
        user_obj.email=email
        user_obj.phone=phone
        user_obj.gender=gender
        user_obj.address = address
        user_obj.last_name=last_name
        user_obj.first_name=first_name
        user_obj.middle_name=middle_name
        user_obj.identification_document = identification_document
        user_obj.identification_document_number = identification_document_number
        user_obj.save()

        print("User Object saved")

        staff_type_names = list(StaffType.objects.filter(id__in=staff_type).values_list('name', flat=True))

        # Create Audit trail for creating staff record
        staff_record = f"""
        <b> <u>Updating Staff Record</u> </b> <br>
        Last Name: {last_name}     | Email:{email}         | Phone: {phone}     
        First Name: {first_name}   | Gender: {gender}      | Address: {address} 
        Middle Name: {middle_name} | Town: {town}
        <br>       
        ID Num: {identification_document_number} | 
        ID Doc: {identification_document} | 
        Sfatt Type: {staff_type_names} | 
        <br>
        <b>About</b> <br>
        {about}
        """            
        audit_trail = StaffAuditTrail.objects.create(
            staff = staff,
            action = "Update",
            action_by = request.user,
            description = staff_record                
        )

        return redirect('staff:view-staff', staff_id)

@login_required(login_url='login')    
def activate_staff(request, id):
    try:
        staff = Staff.objects.get(id=id)
        user = staff.user

        user.is_active = True
        user.save()
        record = f"""
            <b>Activating Staff</b> <br>
            Staff Name - {staff.user.first_name} {staff.user.last_name} | <br>
            Staff Number - {staff.staff_number}
        """
        audit_trail = StaffAuditTrail.objects.create(
            staff = staff,
            action = "Activate",
            action_by = request.user,
            description = record
        )

        return redirect('staff:view-staff', staff.id)
    except Exception as e:
        print(f"Error activating sfatt --> {e}")

@login_required(login_url='login')
def deactivate_staff(request, id):
    try:
        staff = Staff.objects.get(id=id)
        user = staff.user

        user.is_active = False
        user.save()
        record = f"""
            <b>Deactivating Staff</b> <br>
            Staff Name - {staff.user.first_name} {staff.user.last_name} | <br>
            Staff Number - {staff.staff_number}
        """
        audit_trail = StaffAuditTrail.objects.create(
            staff = staff,
            action = "Deactivate",
            action_by = request.user,
            description = record
        )

        return redirect('staff:view-staff', staff.id)
    except Exception as e:
        print(f"Error activating sfatt --> {e}")