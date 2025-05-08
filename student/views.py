from django.shortcuts import render

# Create your views here.
def create(request):
    context = {
        "title": "Student",
        "subtitle": "Create"
               }
    return render (request, 'student/create.html', context)