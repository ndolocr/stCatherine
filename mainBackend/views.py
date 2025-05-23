from datetime import datetime

from django.urls import reverse
from django.shortcuts import render 
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate

from user_management.models import User

def home(request):    
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        return redirect('login')
        
def userLogin(request):
    if request.method == 'POST':
        password = request.POST.get('password', None)
        identifier = request.POST.get('username', None)

        print(f"Username --> {identifier}")
        print(f"Passowrd --> {password}")
        try:
            user = User.objects.get(username=identifier)
            print(f"User found --> {user}")
            authenticated_user = authenticate(request, username=user.username, password=password)                                
            print(f"Authenticated User --> {authenticated_user}")

            if authenticated_user is not None:
                print(user.email)
                print("User Authenticated")
                login(request, authenticated_user)
                print("User Logged in")
                return redirect('home-view')
            else:
                current_year = datetime.now().year
                context = {"current_year": current_year,"error_message": "Invalid username or Password"}
                return render(request, 'authentication/login.html', context=context)
            # if '@' in identifier:
            #     user = User.objects.get(email=identifier)
            #     authenticated_user = authenticate(request, email=user.email, password=password)                                
                
            #     if authenticated_user is not None:
            #         print(user.email)
            #         print("User Authenticated")
            #         login(request, authenticated_user)
            #         print("User Logged in")
            #         return redirect('home-view')
            #     else:
            #         current_year = datetime.now().year
            #         context = {"current_year": current_year,"error_message": "Invalid Email or Password"}
            #         return render(request, 'authentication/login.html', context=context)
            # else:
            #     current_year = datetime.now().year
            #     context = {"current_year": current_year,"error_message": "Invalid Email or Password"}
            #     return render(request, 'authentication/login.html', context=context)
        except User.DoesNotExist as u:
            print(f"Error occured while retrieving user --> {u}")
            current_year = datetime.now().year
            context = {"current_year": current_year,"error_message": "Invalid Email or Password"}
            return render(request, 'authentication/login.html', context=context)
        except Exception as e:
            print(f"Error occured while logging in --> {e}")
            current_year = datetime.now().year
            context = {"current_year": current_year,"error_message": "Invalid Email or Password"}
            return render(request, 'authentication/login.html', context=context)
    else:
        if request.user.is_authenticated:            
            return redirect('dashboard:index')

        current_year = datetime.now().year
        context = {"current_year": current_year}
        return render(request, 'authentication/login.html', context=context)