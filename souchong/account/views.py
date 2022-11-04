from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def home(request):
    return render(request,'main/home.html')

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated: #이미 로그인 되어 있으면
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}
    if request.POST:
        print(f"request={request}")
        print(f"request.POST={request.POST}")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    return render(request, 'account/register.html', context)

# def sign_in(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         password = request.POST['password']
#         user = authenticate(request, name=name, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/chart/home')
#         else:
#             return render(request, 'registration/login.html')
    
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