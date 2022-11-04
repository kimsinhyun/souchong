from django.shortcuts import render, redirect
# from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def sign_in(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, name=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chart/home')
        else:
            return render(request, 'registration/login.html')
    
# def sign_up(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/home')
#     else:
#         form = RegisterForm()
#     return render(request, 'registration/sign_up.html', {'form':form})