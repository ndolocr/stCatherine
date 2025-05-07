from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def dashboardIndex(request):
    user = request.user
    context = {"user": user}
    return  render(request, 'dashboard/index.html', context=context)