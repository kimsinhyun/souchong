from django.urls import path
from . import views 
app_name = "account"
urlpatterns = [
    path('<user_id>/',views.account_view, name='view'),
]