from django.shortcuts import render

from user_management.models import Student

# Create your views here.
def create(request):
    context = {"title": "Student","subtitle": "Create"}
    return render (request, 'student/create.html', context)

def index(request):
    # student = Student.objects.all()
    student = [
        {"admissionNumber": "111111", "admittedOn": "1998-01-01", "first_name":"Ann", "last_name":"Chala", "gender":"Female"},
        {"admissionNumber": "222222", "admittedOn": "1998-02-02", "first_name":"Peter", "last_name":"Mumba", "gender":"Male"},
        {"admissionNumber": "333333", "admittedOn": "1998-03-03", "first_name":"Mary", "last_name":"Ngala", "gender":"Female"}
    ]
    context = {"data":student,"title": "Student","subtitle": "View All"}
    return render (request, 'student/index.html', context)