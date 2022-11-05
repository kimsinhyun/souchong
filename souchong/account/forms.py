from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address")
    class Meta:
        model = Account
        fields = ('email','username','password1','password2')
        
    def clean_email(self):      #유효성 검증 method   아래 AccountAuthenticationForm과 같이 한개의 clean 함수만 사용해도 됨.
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in user")
    
    def clean_username(self):      #유효성 검증 method
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already in user")
        
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput) #password 위젯
    class Meta:
        model = Account
        fields = ("email",'password')
    def clean(self):                                          #여러 clean_XX를 만들지 않고 하나의 clean만 만들어도 됨.
        if self.is_valid():
            email       = self.cleaned_data['email']
            password    = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")