from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from user_management.models import User
from user_management.models import Student

from utils.form_validation import validate_date
from utils.form_validation import validate_name
from utils.form_validation import validate_email
from utils.form_validation import validate_gender
from utils.form_validation import is_alphanumeric
from utils.form_validation import validate_phone_num

from utils.user_name import generate_unique_username

# Create your views here.
@login_required(login_url='login')
def create(request):
    try:
        last_admitted_student = Student.objects.order_by('-id').first()
        new_admission_number = int(last_admitted_student.admission_number) + 1
    except Exception as e:
        print("==========================================")
        print(f"Error getting student record to generate next admission number --> {last_admitted_student}")
        print("==========================================")
        new_admission_number = 1

    print("==========================================")
    print(f"Last Addmitted student --> {last_admitted_student}")
    print(f"Their Admission Number --> {new_admission_number}")
    print("==========================================")

    if request.method == 'GET':
        context = {
        "title": "Student",
        "subtitle": "Create",
        "student_open":"open",
        "student_active":"active", 
        "adm_no": new_admission_number        
    }        
        return render (request, 'student/create.html', context)
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        gender = request.POST.get('gender', None)
        last_name = request.POST.get('last_name', None)
        first_name = request.POST.get('first_name', None)
        middle_name = request.POST.get('middle_name', None)
        admission_date = request.POST.get('admission_date', None)
        admission_number = request.POST.get('admission_number', None)

        print("=================================================")
        print("Captured Data!")
        print("=================================================")
        print(f"Email -- > {email}")
        print(f"Phone -- > {phone}")
        print(f"Last Name -- > {last_name}")
        print(f"First Name -- > {first_name}")
        print(f"Middle -- > {middle_name}")
        print(f"Admission Date -- > {admission_date}")
        print(f"Admission Number -- > {admission_number}")


        print("=================================================")
        print("Data Validation Results!")
        print("=================================================")
        print(f"Email Validation --> {validate_email(email)}")
        print(f"Phone Validation --> {validate_phone_num(phone)}")
        print(f"Gender Validation --> {validate_gender(gender)}")
        print(f"Last Name Validation --> {validate_name(last_name)}")
        print(f"First Name Validation --> {validate_name(first_name)}")
        print(f"Middle Name Validation --> {validate_name(middle_name)}")
        print(f"Addmission Date Validation --> {validate_date(admission_date)}")
        print(f"Addmission Number Validation --> {is_alphanumeric(admission_number)}")
        
        # validate form inputs
        context = {                              
            "title": "Student",
            "subtitle": "Create",
            "student_open":"open",
            "student_active":"active",
            "error_message": "Invalid input details"
        }
        if email:
            user = User.objects.get(email=email)
            context["error_message"] = "Email address already used."
            if not validate_email(email):
                return render (request, 'student/create.html', context)
            
        if phone:
            user = User.objects.get(phone=phone)
            if not validate_phone_num(phone):                
                return render (request, 'student/create.html', context)
        
        if middle_name:
            if not validate_name(middle_name):
                return render (request, 'student/create.html', context) 
            
        if not validate_gender(gender):            
            return render (request, 'student/create.html', context) 
        
        if not last_name or not validate_name(last_name):            
            return render (request, 'student/create.html', context)
        
        if not first_name or not validate_name(first_name):
            return render (request, 'student/create.html', context)         
        
        if not admission_date or not validate_date(admission_date):
            return render (request, 'student/create.html', context) 
        
        if not admission_number or not is_alphanumeric(admission_number):
            return render (request, 'student/create.html', context) 
        
        password = f"{last_name}.{first_name}_{admission_number}"
        username = generate_unique_username(first_name, last_name)
        
        print("=================================================")
        print("Validated Data!")
        print("=================================================")
        print(f"Email -- > {email}")
        print(f"Phone -- > {phone}")
        print(f"Password -- > {password}")
        print(f"Username -- > {username}")
        print(f"Last Name -- > {last_name}")
        print(f"First Name -- > {first_name}")
        print(f"Middle Name-- > {middle_name}")
        print(f"Admission Date -- > {admission_date}")
        print(f"Admission Number -- > {admission_number}")
        
        try:
            print("=================================================")
            print("Saving Student Data!")
            print("=================================================")
            user = User.objects.create(
                email=email,
                phone=phone,
                gender=gender,
                username=username,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,                
                password=make_password(password),
                
            )
            print("=================================================")
            print(f"User record --> {user}!")
            print(f"Password --> {user.password}")
            print("=================================================")
            
            student = Student.objects.create(
                user = user,
                created_by = request.user,
                admitted_on = admission_date,
                admission_number = admission_number,
            )

            print("=================================================")
            print(f"Student record --> {student}!")
            print("=================================================")

            return redirect('student:view-all')

        except Exception as e:
            print("=================================================")
            print(f"Error Saving Student Data --> {e}!")
            print("=================================================")
        
@login_required(login_url='login')
def index(request):        
    student = Student.objects.all()    
    context = {
        "data":student,
        "title": "Student",
        "student_open":"open",
        "subtitle": "View All",
        "student_active":"active",        
    }
    return render (request, 'student/index.html', context)