from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def logout(request):
    django_logout(request)
    return redirect('login')