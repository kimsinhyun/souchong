from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
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
            raw_password = form.cleaned_data.get('password1')   #clean_email 등 함수 호출
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exist(request)
            if destination:  #if desitination != None
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    destination = get_redirect_if_exist(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email       = request.POST['email'] 
            password    = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exist(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context['login_form'] = form
    return render(request, "account/login.html", context)
    
def get_redirect_if_exist(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect

def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/account.html", context)

def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("거부된 요청입니다")
    if account.pk != request.user.pk:
        return HttpResponse("거부된 요청입니다 (다른 유저의 프로필입니다)")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # account -> namespace
            # view -> account/urls.py에 있는 name="view"
            return redirect("account:view",user_id=account.pk)
    # POST가 아닌 GET일 경우 (loading page) 혹은 valid하지 않으면 있던 값을 그대로 넣어져 있는 form 제공
    else:
        # 잘 못 입력했을 경우 이전에 적은 내용이 안 사라지게
        form = AccountUpdateForm(
                                    initial = {
                                        "id": account.pk,
                                        "email":account.email,
                                        "username":account.username,
                                        "profile_image":account.profile_image,
                                        "hide_email":account.hide_email,
                                    }
                            )
        context['form'] = form
        # limie size of the image
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context)


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