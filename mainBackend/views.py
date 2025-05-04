from datetime import datetime
from django.shortcuts import render 
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # or your named dashboard URL
    else:
        return redirect('login')
        
def login(request):
    if request.method == "GET":
        current_year = datetime.now().year
        context = {
            "current_year": current_year,
        }
        return render(request, 'authentication/login.html', context=context)